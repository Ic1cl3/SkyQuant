import yfinance as yf


def getData(stock : str, start_date : str, end_date : str, _interval = "1m") -> list[float]:
    data = yf.download(stock, start=start_date, end=end_date, interval=_interval)
    csvData = data.to_csv()
    lines = csvData.split("\n")
    output : list[float] = []
    for i in range(len(lines)):
        # First 6 lines are headers & odd lines are blankspace seperators.
        if i < 6 or i % 2 == 1:
            continue
        # We take item 2 of the comma seperated line for each datapoint line.
        if len(lines[i].split(",")) > 1:
            output.append(float(lines[i].split(",")[1]))
    return output