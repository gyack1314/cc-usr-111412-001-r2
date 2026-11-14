# 来源接口与业务口径

orders.py的balances(data,asof)读取orders与events，按已知时点筛选最新事件修订并按occurred排序。购买和赠额分别进入paid/gift，用量引用order_id与bucket，退款仅减少尚未使用的付费权益，到期事件核对失效量。返回来源事件与权益分类，不计算收入确认。事件字段为id/revision/kind/order_id/occurred/known/tokens，cash使用十进制字符串。

calls.py的cost_rows通过usage引用use事件，核对input+output与事件tokens，按调用发生时的有效期和asof前已知的价格revision匹配供应商成本；未匹配返回mapped=false，不当成零成本。固定价格可表示成low=high的区间。consumption与cash是业务允许的两种分析政策：前者按付费权益实际消耗确认，到期确认余额，后者按收款减退款；赠额没有收入。政策不代表财务合规意见。

输入为UTF-8 JSON，金额为十进制字符串。样例是合成资料，不限定分析数据规模。
