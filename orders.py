"""购买权益事实的已知时点读取与余额分类。"""
from common import latest,money

def balances(data,asof):
    orders={r['order_id']:r for r in data['orders']}
    if len(orders)!=len(data['orders']):raise ValueError('订单身份重复')
    out={k:{'paid':0,'gift':0,'used_paid':0,'used_gift':0,'invalidated':0,'cash':'0','events':[]} for k in orders}
    events=sorted(latest(data['events'],'id',asof),key=lambda e:(e['occurred'],e['id']))
    for e in events:
        if e['occurred']>asof:continue
        if e['order_id'] not in orders:raise ValueError('未知订单引用')
        b=out[e['order_id']];n=e['tokens'];kind=e['kind']
        if type(n) is not int or n<0:raise ValueError('权益量非法')
        if kind=='purchase':b['paid']+=n;b['cash']=str(money(b['cash'])+money(e['cash']))
        elif kind=='grant':b['gift']+=n
        elif kind=='use':
            bucket=e['bucket']
            if bucket not in ('paid','gift') or b[bucket]<n:raise ValueError('权益消耗超过来源')
            if e['occurred']>=orders[e['order_id']]['expires']:raise ValueError('到期后调用权益')
            b[bucket]-=n;b['used_'+bucket]+=n
        elif kind=='refund':
            if b['paid']<n or money(e['cash'])<0:raise ValueError('退款超未用付费权益')
            b['paid']-=n;b['cash']=str(money(b['cash'])-money(e['cash']))
        elif kind=='expire':
            if e['occurred']<orders[e['order_id']]['expires']:raise ValueError('提前失效')
            if n!=b['paid']+b['gift']:raise ValueError('失效量不符')
            b['invalidated']+=n;b['paid']=b['gift']=0
        else:raise ValueError('未知权益事实')
        b['events'].append(e['id'])
    return out
