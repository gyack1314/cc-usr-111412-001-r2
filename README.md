# 预付智能服务的履约成本预测与同群收入分析

项目提供智能消费业务分析使用的来源准备接口。记录为合成资料，不对应真实平台客户。orders.py只重放已知权益事实，calls.py给已实现调用的成本输入。尚无收入确认政策、cohort单位经济或未来成本情景引擎。

`orders.py`、`calls.py`负责实际资料语义，`analytics.py`调用这些接口形成当前可用输入。`common.py`提供精确金额、时点修订读取和摘要绑定的不可变发布。来源字段与语义见[资料契约](docs/contracts.md)。

运行环境为Python 3.11，当前依赖仅标准库。以下命令在项目根目录执行：

```sh
python -m unittest discover -s tests -v
python -m compileall -q .
python -m analytics
```

Linux环境也可执行：

```sh
docker build -t intelligent-consumption .
docker run --rm --network=none intelligent-consumption
docker run --rm --network=none intelligent-consumption python -m analytics
```

运行创建的报告和临时文件使用`.runtime/`，不将本机账号配置写入项目。

fulfillment.py的order_histories按订单与account保留连续覆盖范围、到期日、实际调用及付费/赠额来源，不包含未来购买或未来消耗预测。coverage_end定义已知连续日志覆盖终点，超过此点是未观察，不是0。供应商未来价格仅作为冻结情景，不将未来修订当成当时已知。
