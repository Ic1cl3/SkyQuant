import dataGetter as dg

class market:

    prices : dict[str , float]
    timestep : int
    data : dict[str, list[float]]

    def __init__(self) -> None:
        self.prices = {}
        self.timestep = -1
        self.data = {}
        stocks = []
        with open("config/stockList.txt", "r") as f:
            for line in f:
                stock = line.strip()
                stocks.append(stock)
        starts = []
        ends = []
        timestep = ""
        with open("config/dates.txt", "r") as f:
            starts = f.readline().strip().split(",")
            ends = f.readline().strip().split(",")
            timestep = f.readline().strip()
        for stock in stocks:
            stockData = []
            for pointIndex in range(len(starts)):
                for point in dg.getData(stock, starts[pointIndex], ends[pointIndex], timestep):
                    stockData.append(point)
            self.data[stock] = stockData
        self.update()

    def update(self) -> None:
        self.timestep += 1
        for stock in self.data:
            self.prices[stock] = self.data[stock][self.timestep]