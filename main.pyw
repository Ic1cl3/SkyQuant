from tkinter import *
from tkinter import ttk

root = Tk()
root.title("SkyQuant")
root.iconbitmap("icon.ico")
root.maxsize(700, 500)
root.minsize(700, 500)
frame = ttk.Frame(root, padding=20, width="700px",height="700px")
ttk.Label(frame, text="FU").place(x=100, y=100, relwidth=1.0, relheight=1.0)
root.mainloop()