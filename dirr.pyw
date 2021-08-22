from tkinter import *
from os import popen
root = Tk()
root.title("显示目录下的文件")
root.geometry("1000x700")
with popen("dir /a /q", "r") as p:
    Label(text=p.read()).pack(side=TOP)
mainloop()
