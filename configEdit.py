def getStockList(data : str) -> str:
    with open("config/stockList.txt", "r") as f:
        return f.read()

def updateStockList(data : str) -> None:
    with open("config/stockList.txt", "w") as f:
        f.write(str)
        f.close()

def getDates(data : str) -> str:
    with open("config/dates.txt", "r") as f:
        return f.read()

def updateDates(data : str) -> None:
    with open("config/dates.txt", "w") as f:
        f.write(str)
        f.close()