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
        start = ""
        end = ""
        timestep = ""
        with open("config/dates.txt", "r") as f:
            start = f.readline().strip()
            end = f.readline().strip()
            timestep = f.readline().strip()
        for stock in stocks:
            self.data[stock] = dg.getData(stock, start, end, timestep)
        self.update()

    def update(self) -> None:
        self.timestep += 1
        for stock in self.data:
            self.prices[stock] = self.data[stock][self.timestep]