"""当前资料的准备入口，不含目标分析模型。"""
import json
from common import read
from orders import balances
from calls import cost_rows
from fulfillment import order_histories
def prepare():
    data=read()
    return {'order_histories':order_histories(data,data['asof']),'balances':balances(data,data['asof']),'cost_inputs':cost_rows(data,data['asof'])}
if __name__=="__main__":print(json.dumps(prepare(),ensure_ascii=False,indent=2))
