"""调用修订与供应商价格有效期查询。"""
from common import latest,money

def cost_rows(data,asof):
    calls=latest(data['calls'],'id',asof);out=[]
    for c in calls:
        if min(c['input'],c['output'])<0:raise ValueError('调用计量为负')
        events=[e for e in latest(data['events'],'id',asof) if e['id']==c['usage'] and e['kind']=='use']
        if len(events)!=1:raise ValueError('调用缺少唯一已知权益事实')
        e=events[0]
        if c['input']+c['output']!=e['tokens']:raise ValueError('调用与权益单位不一致')
        candidates=[r for r in data['rates'] if r['model']==c['model'] and r['known']<=asof and r['start']<=e['occurred']<r['end']]
        if not candidates:out.append({'call':c['id'],'order':e['order_id'],'mapped':False});continue
        rev=max(r['revision'] for r in candidates);rates=[r for r in candidates if r['revision']==rev]
        if len(rates)!=1:raise ValueError('同版本价格区间冲突')
        r=rates[0];low=money(r['input_low'])*c['input']+money(r['output_low'])*c['output'];high=money(r['input_high'])*c['input']+money(r['output_high'])*c['output']
        if low<0 or high<low:raise ValueError('价格范围非法')
        out.append({'call':c['id'],'order':e['order_id'],'mapped':True,'low':str(low),'high':str(high),'rate_revision':rev})
    return out
