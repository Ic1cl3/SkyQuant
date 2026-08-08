from predictor import predictor

# This strategy looks at very recent trends to predict ultra high frequency movements.
class strategyB(predictor):

    def call(self) -> None:
        for stock in self.market.prices:
            prediction = 0
            for i in range(min(9, self.market.timestep)):
                if i < 1:
                    continue
                if self.market.data[stock][self.market.timestep-i] > self.market.data[stock][self.market.timestep-i-1]:
                    prediction += 1
            print(f"{stock}: {prediction}")
            if prediction < 8: continue
            if prediction > 0:
                self.buy(stock, 30)
            else:
                self.sell(stock, 30)