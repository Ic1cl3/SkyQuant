import market as mk

class trader:

    balance : int
    holdings : dict[str , int]
    market : mk.market

    def __init__(self, balance : int, market : mk.market) -> None:
        self.balance = balance
        self.holdings = {}
        self.market = market

    def buy(self, stock : str, quantity : int) -> bool:
        price = self.market.prices[stock]
        total_cost = quantity * price
        if self.balance >= total_cost:
            self.balance -= total_cost
            if stock in self.holdings:
                self.holdings[stock] += quantity
            else:
                self.holdings[stock] = quantity
            return True
        else:
            return False

    def sell(self, stock : str, quantity : int) -> bool:
        price = self.market.prices[stock]
        if stock in self.holdings and self.holdings[stock] >= quantity:
            total_revenue = quantity * price
            self.balance += total_revenue
            self.holdings[stock] -= quantity
            if self.holdings[stock] == 0:
                del self.holdings[stock]
            return True
        else:
            return False

    def sellAll(self, stock : str = None):
        if stock is None:
            # Sell all holdings
            for stock in list(self.holdings.keys()):
                self.sellAll(stock)
            return True
        self.sell(stock, self.holdings[stock])

    def short(self, stock : str, quantity : int) -> bool:
        price = self.market.prices[stock]
        total_cost = quantity * price
        if self.balance >= total_cost:
            self.balance -= total_cost
            if stock in self.holdings:
                self.holdings[stock] -= quantity
            else:
                self.holdings[stock] = -quantity
            return True
        else:
            return False

    def evaluate(self) -> float:
        portfolioValue = self.balance
        for stock in self.holdings:
            portfolioValue += self.holdings[stock] * self.market.prices[stock]
        return portfolioValue