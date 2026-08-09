from tkinter import *
import tkinter
from tkinter import ttk
from pathlib import Path


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


scriptdir = Path(__file__).parent
# Root window generation.
root = Tk()
root.geometry=("900x500")
root.title("SkyQuant")
root.iconbitmap(str(scriptdir) + "/icon.ico")
root.maxsize(900, 500)
root.minsize(900, 500)
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
# Build.
root.mainloop()