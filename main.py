from tkinter import *
import tkinter
from tkinter import ttk
from pathlib import Path
import configEdit as cE
import time
import market as mk
import predictor
from strategies import strategyA as sA
from strategies import strategyB as sB


# Stylized lables.
class sLabel(ttk.Label):

    def style(self):
        self["background"] = "#1F2539"
        self["foreground"] = "white"
        self["font"] = ("Courier", 20, "bold")

# Stylized buttons.
class sButton(Button):

    def style(self):
        self["bg"] = "#1F2539"
        self["activebackground"] = "#343e60"
        self["fg"] = "white"
        self["activeforeground"] = "white"
        self["font"] = ("Courier", 12, "normal")
        self["relief"] = "flat"

# Stylized entries.
class sEntry(Entry):

    def style(self):
        self["bg"] = "#343e60"
        self["fg"] = "white"
        self["font"] = ("Courier", 12, "normal")
        self["width"] = 20
        self["insertbackground"] = "white"


# Enum
stratA = 0
stratB = 1
stratC = 2
stratD = 3
# Strategy selection tracking.
strategy : int = 1
def keepFlat(event) -> None:
    global selLine
    global strategy
    global root
    event.widget.config(relief=FLAT)
    selectionPositions = {
        0 : (30, 130),
        1 : (160, 130),
        2 : (30, 170),
        3 : (160, 170)
    }
    but = event.widget
    if but["text"] == "Strategy A":
        chooseA()
    if but["text"] == "Strategy B":
        chooseB()
    if but["text"] == "Strategy C":
        chooseC()
    if but["text"] == "Strategy D":
        chooseD()
    selLine.place(x=selectionPositions[strategy][0], y=selectionPositions[strategy][1], anchor="nw")
    updateStratDesc()
    root.mainloop()
def chooseA() -> None:
    global strategy
    strategy = stratA
def chooseB() -> None:
    global strategy
    strategy = stratB
def chooseC() -> None:
    global strategy
    strategy = stratC
def chooseD() -> None:
    global strategy
    strategy = stratD
def updateStratDesc() -> None:
    global stratDesc
    global strategy
    global root
    descriptions = {
        0 : "Uses correlation and similar trends between stocks to detect market mispricings. Best for low-frequency trading within a tight, stable industry.",
        1 : "Uses ultra-short term data for ultra-high frequency trades by analyzing microtrends.",
        2 : "Uses machine learning to detect recurring price patterns. Works decently on any frequency. (Unfinished)",
        3 : "Uses ultra-short term data for ultra-high frequency trades by analyzing calculus of other prices' impact. (Unfinished)"
    }
    stratDesc.config(text=descriptions[strategy])
    root.update()

# Compiling config data.
def configure() -> None:
    global startDates
    global endDates
    global timeScale
    global stocks
    stockLines = ""
    for stock in stocks.get().split(","):
        stockLines += stock + "\n"
    stockLines = stockLines[:len(stockLines) - 1]
    cE.updateStockList(stockLines)
    timelines = ""
    timelines += startDates.get() + "\n"
    timelines += endDates.get() + "\n"
    timelines += timeScale.get()
    cE.updateDates(timelines)
def fetch() -> None:
    global startDates
    global endDates
    global timeScale
    global stocks
    stockCommas = ""
    for stock in cE.getStockList().split("\n"):
        stockCommas += stock + ","
    stockCommas = stockCommas[:len(stockCommas) - 1]
    stocks.insert(string=stockCommas, index=0)
    timeData = cE.getDates().split("\n")
    startDates.insert(string=timeData[0], index = 0)
    endDates.insert(string=timeData[1], index=0)
    timeScale.insert(string=timeData[2], index=0)

# Run stuff.
def graphPortfolio(portfolio : list[float]) -> None:
    global graph
    global stats
    global skyLabel
    global highL
    global lowL
    horStep = 540/(len(portfolio) - 1)
    graph.delete("trendline")
    high = 11000
    low = 9000
    for value in portfolio:
        if value >= high:
            high = value
        if value <= low:
            low = value
    if abs(10000-low) > abs(10000-high):
        high = 10000+abs(10000-low)
    elif abs(10000-high) > abs(10000-low):
        low = 10000-abs(10000-high)
    valueRange = high - low
    position = (0, portfolio[0])
    for i in range(len(portfolio)):
        if i == 0: continue
        color = "red"
        if portfolio[i] > position[1]:
            color = "green"
        graph.create_line(position[0]*horStep, 400*(1-((position[1]-low)/valueRange)), i*horStep, 400*(1-((portfolio[i]-low)/valueRange)), fill=color, width=5, tags="trendline", capstyle="round")
        stats["text"] = f"Value: ${round(portfolio[i],2)}; Profit: {round((round(100*(portfolio[i]/10000), 2))-100, 2)}%"
        if portfolio[i] > 10000:
            skyLabel["text"] = "You have broken through the clouds."
            skyLabel["foreground"] = "green"
        else:
            skyLabel["text"] = "Find more familiar skies."
            skyLabel["foreground"] = "red"
        lowL["text"] = f"${round(low, 2)}"
        highL["text"] = f"${round(high, 2)}"
        position = (i, portfolio[i])

def hist() -> None:
    global graph
    global strategy
    global root
    configure()
    graph.delete("trendline")
    market = mk.market()
    trader = None
    if strategy == stratA:
        trader = sA.strategyA(10000, market)
    if strategy == stratB:
        trader = sB.strategyB(10000, market)
    if strategy == stratC or strategy == stratD:
        trader = predictor.predictor(10000, market)
    history = [10000 for i in range(50)]
    for i in range(20):
        market.update()
    length = -1
    for key in market.data:
        if len(market.data[key]) < length or length == -1:
            length = len(market.data[key])
    for i in range(length - 25):
        trader.call()
        market.update()
        history.pop(0)
        history.append(trader.evaluate())
        graphPortfolio(history)
        root.update()
        time.sleep(0)

def paper() -> None:
    configure()

scriptdir = Path(__file__).resolve().parent
# Root window generation.
root = Tk()
root.geometry=("900x500")
root.title("SkyQuant")
root.iconbitmap(str(scriptdir) + "/icon.ico")
root.maxsize(910, 550)
root.minsize(910, 550)
root["bg"] = "#1F2539"
# Content creation.
## Title
title = sLabel(root, text="SkyQuant")
title.style()
title.place(x=20, y=20, anchor="nw")
line = Canvas(root, width=150, height=3, background="#1F2539", highlightthickness=0, borderwidth=0)
line.create_line(0, 0, 150, 0, width=3, fill="white")
line.place(x=20, y=58, anchor="nw")
## Strategy selection.
heading1 = sLabel(root, text="Choose strategy:")
heading1.style()
heading1["font"] = ("Courier", 15, "normal")
heading1.place(x=20,y=67, anchor="nw")
selectorA = sButton(root, text="Strategy A")
selectorA.style()
selectorA.bind("<Button-1>", keepFlat)
selectorA.place(x=20, y=100, anchor="nw")
selectorB = sButton(root, text="Strategy B")
selectorB.style()
selectorB.place(x=150, y=100, anchor="nw")
selectorB.bind("<Button-1>", keepFlat, add="+")
selectorC = sButton(root, text="Strategy C")
selectorC.style()
selectorC.place(x=20, y=140, anchor="nw")
selectorC.bind("<Button-1>", keepFlat, add="+")
selectorD = sButton(root, text="Strategy D")
selectorD.style()
selectorD.place(x=150, y=140, anchor="nw")
selectorD.bind("<Button-1>", keepFlat, add="+")
selLine = Canvas(root, width=90, height=3, background="#1F2539", highlightthickness=0, borderwidth=0)
selLine.create_line(0, 0, 90, 0, width=3, fill="white")
selLine.place(x=160, y=130, anchor="nw")
stratDesc = sLabel(root, text="Uses ultra-short term data for ultra-high frequency trades by analyzing microtrends.", width=250, wraplength=250)
stratDesc.style()
stratDesc["font"] = ("Courier", 14, "normal")
stratDesc.place(x=20, y=185, anchor="nw")
## Sim edit.
simEditLabel = sLabel(root, text="Edit Config:")
simEditLabel.style()
simEditLabel["font"] = ("Courier", 12, "normal")
simEditLabel.place(x=20, y=360)
startDates = sEntry(root)
startDates.style()
startDates.place(x=20, y=385)
endDates = sEntry(root)
endDates.style()
endDates.place(x=20,y=405)
timeScale = sEntry(root)
timeScale.style()
timeScale.place(x=20,y=425)
stocks = sEntry(root)
stocks.style()
stocks.place(x=20,y=445)
runSim = sButton(root, text="Simulate Historical Data", padx=0, pady=0, command=hist)
runSim.style()
runSim["font"] = ("Courier", 12, "normal")
runSim["relief"] = "raised"
runSim
runSim.place(x=18, y=470)
trade = sButton(root, text="Trade Paper", padx=0, pady=0, command=paper)
trade.style()
trade["font"] = ("Courier", 12, "normal")
trade["relief"] = "raised"
trade.place(x=18, y=500)
fetch()
# Graph.
graph = Canvas(root, width=540, height=400, background="#343e60", highlightthickness=0)
graph.place(x=300, y=80, anchor="nw")
graph.create_line(0, 200, 540, 200, width=5, fill="#1F2539")
highL = sLabel(root, text="$11000.00")
lowL = sLabel(root, text="$9000.00")
highL.style()
lowL.style()
highL["font"] = ("Courier", 8, "normal")
lowL["font"] = ("Courier", 8, "normal")
highL.place(x=842, y=80, anchor="nw")
lowL.place(x=842, y=480, anchor="sw")
midL = sLabel(root, text="Sky High\n$10000.00")
midL.style()
midL["font"] = ("Courier", 8, "normal")
midL.place(x=842,y=275,anchor="w")
skyLabel = sLabel(root, text="Find more familiar skies.")
skyLabel.style()
skyLabel["foreground"] = "red"
skyLabel.place(x=310, y=490, anchor="nw")
stats = sLabel(root, text = "Value: $10000.00; Profit: 0.00%")
stats.style()
stats.place(x=310,y=70,anchor="sw")
# Build.
root.mainloop()