import trader as td
import market as mk

market = mk.market()
trader = td.trader(10000, market)

avgPriceMcd = 0
for i in range(90):
    avgPriceMcd += market.data["MCD"][i]
avgPriceMcd /= 90


for i in range(90):
    if market.prices["MCD"] < avgPriceMcd:
        trader.buy("MCD", 1)
    elif market.prices["MCD"] > avgPriceMcd:
        trader.sell("MCD", 1)
    market.update()
trader.sellAll()
print(trader.balance)