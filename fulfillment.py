"""固定订单的实际履约历史，不拟合未来消耗。"""
from orders import balances
from common import latest

def order_histories(data,asof):
    state=balances(data,asof);events=latest(data['events'],'id',asof);calls=latest(data['calls'],'id',asof);out=[]
    for order in data['orders']:
        rows=[e for e in events if e['order_id']==order['order_id'] and e['occurred']<=asof]
        paid=[e for e in rows if e['kind']=='purchase']
        if not paid:continue
        start=min(e['occurred'] for e in paid);end=min(asof,order['expires'],order.get('coverage_end',asof))
        if end<start:raise ValueError('履约观察范围非法')
        by_id={e['id']:e for e in rows if e['kind']=='use' and e['occurred']<=end}
        observations=[]
        for call in calls:
            if call['usage'] not in by_id:continue
            event=by_id[call['usage']]
            observations.append({'call_id':call['id'],'day':event['occurred'],'model':call['model'],'bucket':event['bucket'],'input':call['input'],'output':call['output']})
        out.append({'order_id':order['order_id'],'account':order['account'],'cohort':order['cohort'],'observed_from':start,'observed_through':end,'expires':order['expires'],'remaining_at_asof':state[order['order_id']],'calls':observations,'events':[e for e in rows if e['occurred']<=end]})
    return out
