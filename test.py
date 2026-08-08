import trader as td
from strategies import strategyA as sA
import market as mk
import dataGetter as dg

market = mk.market()
trader = sA.strategyA(10000, market)

for i in range(20):
    market.update()

for i in range(160):
    trader.call()
    market.update()
    print(market.timestep, trader.balance)

trader.sellAll()
print("Final balance:", trader.balance)