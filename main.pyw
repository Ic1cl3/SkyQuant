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
        self["borderwidth"] = 2
        self["relief"] = "flat"


# Enum
stratA = 0
stratB = 1
stratC = 2
stratD = 3
# Strategy selection tracking.
strategy : int = 1
def keepFlat(event) -> None:
    print("1")
    event.widget.config(relief=FLAT)
    print("2")
    root.mainloop()
def chooseA() -> None:
    strategy = stratA
def chooseB() -> None:
    strategy = stratB
def chooseC() -> None:
    strategy = stratC
def chooseD() -> None:
    strategy = stratD


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
selectorA = sButton(root, text="Strategy A", command=chooseA)
selectorA.style()
selectorA.place(x=20, y=100, anchor="nw")
selectorA.bind("<Button-1>", keepFlat)
# Build.
root.mainloop()