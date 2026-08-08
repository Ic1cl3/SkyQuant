from predictor import predictor

# This strategy looks at very recent trends to predict ultra high frequency movements.
class strategyB(predictor):

    def call(self) -> None:
        for stock in self.market.prices:
            prediction = 0
            # Retrieve some recent data for each stock.
            averagePrice = 0
            start = self.market.data[stock][self.market.timestep - 9]
            end = self.market.data[stock][self.market.timestep]
            high = 0.0
            low = self.market.data[stock][self.market.timestep]
            for i in range(9):
                point = self.market.data[stock][self.market.timestep - i]
                if point > high:
                    high = point
                if point < low:
                    low = point
                averagePrice += point
            averagePrice /= 9
            pRange = high - low
            trend = ((end/pRange) - (start/pRange))
            prediction = (trend * 1.5)**3
            print(f"{stock}: {prediction}")
            if abs(prediction) < 0.8: continue
            budget = round(prediction * 300) - self.market.prices[stock]
            while budget > 0:
                if prediction > 0:
                    self.buy(stock, 1)
                else:
                    self.sell(stock, 1)
                budget -= self.market.prices[stock]