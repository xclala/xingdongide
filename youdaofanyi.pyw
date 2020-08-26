from tkinter import *
try:
    import requests
    from tkinter.scrolledtext import ScrolledText
    top = Tk()
    top.title("翻译器")
    top.geometry('500x30')

    def fanyi():
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': string.get()
        }
        url = "http://fanyi.youdao.com/translate"
        r = requests.get(url, params=data)
        result = r.json()
        translate_result = result['translateResult'][0][0]["tgt"]
        l = Label(text="翻译结果:"+translate_result)
        l.pack(side=LEFT)
    label = Label(text='请输入文字:')
    label.pack(side=LEFT)
    c = ScrolledText()
    string = Entry()
    string.pack(side=LEFT, expand=True, fill=X)
    Button(text='转换', command=fanyi).pack(side=RIGHT)
    mainloop()
except:
    pass
