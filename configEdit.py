from pathlib import Path
import sys

scriptPath = None

scriptPath = str(Path(__file__).resolve().parent)

def getStockList() -> str:
    with open(scriptPath + "\\config\\stockList.txt", "r") as f:
        output = f.read()
        f.close()
        return output

def updateStockList(data : str) -> None:
    with open(scriptPath + "\\config\\stockList.txt", "w") as f:
        f.write(data)
        f.close()

def getDates() -> str:
    with open(scriptPath + "\\config\\dates.txt", "r") as f:
        output = f.read()
        f.close()
        return output

def updateDates(data : str) -> None:
    with open(scriptPath + "\\config\\dates.txt", "w") as f:
        f.write(data)
        f.close()