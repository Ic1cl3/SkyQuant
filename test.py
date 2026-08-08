import trader as td
from strategies import strategyA as sA
from strategies import strategyB as sB
import market as mk
import dataGetter as dg

market = mk.market()
trader = sB.strategyB(10000, market)

for i in range(20):
    market.update()

for i in range(1000):
    trader.call()
    market.update()
    print(market.timestep, trader.balance)

trader.sellAll()
print("Final balance:", trader.balance)