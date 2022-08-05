from tkinter import *
from subprocess import run, PIPE

root = Tk()
root.title("显示目录下的文件")
root.geometry("1000x700")
_ = run(["dir", "/a", "/q"], shell=True, stdout=PIPE)
Label(text=_.stdout.decode("gb2312")).pack(side=TOP)
mainloop()
