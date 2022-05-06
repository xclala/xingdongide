try:
    from tkinter import *
    from os import popen
    root = Tk()
    root.title("目录结构")
    root.geometry("1000x750")

    def main_keyboard(event):
        if str(i.get()) == '':
            with popen("tree", "r") as p:
                Label(text=p.read()).pack(side=TOP)
        else:
            with popen("tree " + i.get(), "r") as p:
                Label(text=p.read()).pack(side=TOP)

    def main():
        if str(i.get()) == '':
            with popen("tree", "r") as p:
                Label(text=p.read()).pack(side=TOP)
        else:
            with popen("tree " + i.get(), "r") as p:
                Label(text=p.read()).pack(side=TOP)

    i = Entry(width=100, font=40)
    i.pack(side=TOP)
    root.bind("<Return>", main_keyboard)
    Button(text='显示', command=main).pack()
    mainloop()
except:
    pass
