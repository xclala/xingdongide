from tkinter import *
try:
    from requests import get
    from tkinter.scrolledtext import ScrolledText
    from tkinter import messagebox
    top = Tk()
    top.title("翻译器")
    top.geometry('500x30')

    def translate():
        data = {'doctype': 'json', 'type': 'AUTO', 'i': string.get()}
        url = "http://fanyi.youdao.com/translate"
        result = get(url, params=data).json()
        translate_result = result['translateResult'][0][0]["tgt"]
        messagebox.showinfo(title='翻译结果', message=translate_result)

    label = Label(text='请输入文字:')
    label.pack(side=LEFT)
    c = ScrolledText()
    string = Entry()
    string.pack(side=LEFT, expand=True, fill=X)
    Button(text='转换', command=translate).pack(side=RIGHT)
    mainloop()
except Exception as e:
    print(e)
