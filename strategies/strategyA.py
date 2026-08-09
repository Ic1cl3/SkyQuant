from math import floor
from predictor import predictor

# This strategy looks at correlation between stocks.
# Similar stocks (e.g. mcdonalds and wendy's) trend together.
# If an anomoly occurs, we predict that it is a mispricing and will correct.
# Works better on relatively lower frequency time scales.
class strategyA(predictor):

    def call(self) -> None:
        for stock1 in self.market.prices:
            prediction = 0
            for stock2 in self.market.prices:
                if stock1 == stock2 or self.market.timestep < 10:
                    continue
                # Find correlation and standard deviation.
                stock1trend = []
                stock2trend = []
                for i in range(min(50, self.market.timestep)):
                    if i < 1:
                        continue
                    stock1trend.append(self.market.data[stock1][i]/self.market.data[stock1][i-1])
                    stock2trend.append(self.market.data[stock2][i]/self.market.data[stock2][i-1])
                stock1OverallTrend = 0
                stock2OverallTrend = 0
                for i in range(len(stock1trend)):
                    stock1OverallTrend += stock1trend[i]
                    stock2OverallTrend += stock2trend[i]
                stock1OverallTrend /= len(stock1trend)
                stock2OverallTrend /= len(stock2trend)
                correlation = 0
                correlationDatapoints = []
                for i in range(len(stock1trend)):
                    correlation += abs(stock1trend[i] - stock2trend[i])
                    correlationDatapoints.append(abs(stock1trend[i] - stock2trend[i]))
                correlation /= len(stock1trend)
                deviationSum = 0
                for datapoint in correlationDatapoints:
                    deviationSum += (datapoint - correlation) ** 2
                deviationSum /= (len(correlationDatapoints) - 1)
                standardDeviation = deviationSum ** 0.5
                # Correlation is the average difference between the factor by which each stock scales each timestep.
                # We now calculate how correlations have recently trended, as well as how each stock has.
                recentCorrelation = 0
                recentTrend = 0
                recentPairTrend = 0
                for i in range(floor(len(correlationDatapoints)/5)):
                    recentCorrelation += correlationDatapoints[-(i+1)]
                    recentTrend += stock1trend[-(i+1)]
                    recentPairTrend += stock2trend[-(i+1)]
                recentCorrelation /= floor(len(correlationDatapoints)/5)
                recentTrend /= floor(len(correlationDatapoints)/5)
                recentPairTrend /= floor(len(correlationDatapoints)/5)
                recentTrendChange = recentTrend/stock1OverallTrend
                recentPairTrendChange = recentPairTrend/stock2OverallTrend
                # Using a combination of information on divergence and trend differences, we predict.
                readjustmentFactor = -1
                if recentCorrelation < correlation:
                    # If we are becoming more correlated (lower = more), predict trends to match up.
                    readjustmentFactor = 1
                confidence = ((abs(recentCorrelation - correlation)/standardDeviation)**1.5) * ((recentTrendChange/recentPairTrendChange)**1.5)
                prediction += readjustmentFactor * confidence * (recentTrend)
            if prediction > 0:
                for i in range(round(prediction*3)):
                    self.buy(stock1, 1)
            else:
                for i in range(round(prediction*3)):
                    self.sell(stock1, 1)