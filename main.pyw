from tkinter import *
import tkinter
from tkinter import ttk
from pathlib import Path
import configEdit as cE


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
def hist():
    configure()
def paper():
    configure()

scriptdir = Path(__file__).parent
# Root window generation.
root = Tk()
root.geometry=("900x500")
root.title("SkyQuant")
root.iconbitmap(str(scriptdir) + "/icon.ico")
root.maxsize(900, 550)
root.minsize(900, 550)
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
trade
trade.place(x=18, y=500)
fetch()
# Build.
root.mainloop()