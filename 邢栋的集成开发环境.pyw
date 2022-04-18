try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
    from os import system, getcwd, popen
    import string
    from keyword import kwlist
    from threading import Thread
    from win32com.shell import shell, shellcon

    def hook_dropfiles(tkwindow_or_winfoid, func, force_unicode=False):
        import platform
        import ctypes
        from ctypes.wintypes import DWORD

        hwnd = tkwindow_or_winfoid.winfo_id()\
            if getattr(tkwindow_or_winfoid, "winfo_id", None)\
            else tkwindow_or_winfoid

        if platform.architecture()[0] == "32bit":
            GetWindowLong = ctypes.windll.user32.GetWindowLongW
            SetWindowLong = ctypes.windll.user32.SetWindowLongW
            argtype = DWORD
        elif platform.architecture()[0] == "64bit":
            GetWindowLong = ctypes.windll.user32.GetWindowLongPtrA
            SetWindowLong = ctypes.windll.user32.SetWindowLongPtrA
            argtype = ctypes.c_uint64

        prototype = ctypes.WINFUNCTYPE(argtype, argtype, argtype, argtype,
                                       argtype)
        WM_DROPFILES = 0x233
        GWL_WNDPROC = -4
        create_buffer = ctypes.create_unicode_buffer if force_unicode else ctypes.c_buffer
        func_DragQueryFile = ctypes.windll.shell32.DragQueryFileW if force_unicode else ctypes.windll.shell32.DragQueryFile

        def py_drop_func(hwnd, msg, wp, lp):
            global files
            if msg == WM_DROPFILES:
                count = func_DragQueryFile(argtype(wp), -1, None, None)
                szFile = create_buffer(260)
                files = []
                for i in range(count):
                    func_DragQueryFile(argtype(wp), i, szFile,
                                       ctypes.sizeof(szFile))
                    dropname = szFile.value
                    files.append(dropname)
                func(files)
                ctypes.windll.shell32.DragFinish(argtype(wp))
            return ctypes.windll.user32.CallWindowProcW(
                *map(argtype, (globals()[old], hwnd, msg, wp, lp)))

        # for limit hook number, protect computer.
        limit_num = 200
        for i in range(limit_num):
            if i + 1 == limit_num:
                raise "over hook limit number 200, for protect computer."
            if "old_wndproc_%d" % i not in globals():
                old, new = "old_wndproc_%d" % i, "new_wndproc_%d" % i
                break

        globals()[old] = None
        globals()[new] = prototype(py_drop_func)

        ctypes.windll.shell32.DragAcceptFiles(hwnd, True)
        globals()[old] = GetWindowLong(hwnd, GWL_WNDPROC)
        SetWindowLong(hwnd, GWL_WNDPROC, globals()[new])

    def load():
        from win32ui import CreateFileDialog
        from win32con import OFN_OVERWRITEPROMPT, OFN_FILEMUSTEXIST
        file_open_type = 'All File(*.*)|*.*|'\
            'HTML File(*.html)|*.html|'\
            'Python File(*.py .pyw)|*.py;*.pyw|'\
            'C File(*.c *.h) |*.c;*.h|'\
            'Go File(*.go) |*.go|'\
            'Java File(*.java)|*.java|'\
            'Batch File(*.bat *.cmd) |*.bat;*.cmd|'\
            '|'
        d = CreateFileDialog(1, None, None,
                             OFN_OVERWRITEPROMPT | OFN_FILEMUSTEXIST,
                             file_open_type)
        d.SetOFNInitialDir('C:/')
        d.DoModal()
        with open(d.GetPathName(), encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title("打开" + message.get())

    def dragged_load(files):
        msg = files[0].decode("gbk")
        with open(msg, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title("打开" + msg)

    def save():
        from win32ui import CreateFileDialog
        from win32con import OFN_OVERWRITEPROMPT, OFN_FILEMUSTEXIST
        file_save_type = 'All File(*.*)|*.*|'\
            'HTML File(*.html)|*.html|'\
            'Python File(*.py .pyw)|*.py;*.pyw|'\
            'C File(*.c *.h) |*.c;*.h|'\
            'Go File(*.go) |*.go|'\
            'Java File(*.java)|*.java|'\
            'Batch File(*.bat) |*.bat|'\
            '|'
        dd = CreateFileDialog(0, None, None,
                              OFN_OVERWRITEPROMPT | OFN_FILEMUSTEXIST,
                              file_save_type)
        dd.SetOFNInitialDir('C:/')
        dd.DoModal()
        with open(dd.GetPathName(), 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("保存" + message.get())

    def python_save():
        with open(message.get() + ".py", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以命令行的python格式保存" + message.get())

    def pythonw_save():
        with open(message.get() + ".pyw", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以可视化的python格式保存" + message.get())

    def c_save():
        with open(message.get() + ".c", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以c语言的格式保存")

    def cpp_save():
        with open(message.get() + ".cpp", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以c++语言的格式保存")

    def go_save():
        with open(message.get() + ".go", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以go语言的格式保存")

    def java_save():
        with open(message.get() + ".java", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以java语言的格式保存")

    def html_save():
        with open(message.get() + ".htm", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以html的格式保存")

    def h_save():
        with open(message.get() + ".h", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以c语言头文件的格式保存")

    def bat_save():
        with open(message.get() + ".bat", 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("以批处理文件的格式保存")

    def md():
        from os import mkdir
        mkdir(message.get())

    def rd():
        from os import rmdir
        rmdir(message.get())

    def mds():
        from os import makedirs
        makedirs(message.get())

    def rds():
        from os import removedirs
        removedirs(message.get())

    def python_cache():
        from os import removedir
        removedir("__pycache__")

    def pip_install():
        top.title("用pip安装" + message.get())
        system("pip install " + message.get() + " --no-cache-dir & pause")

    def pip_upgrade():
        top.title("用pip升级" + message.get())
        system("pip install --upgrade " + message.get() +
               " --no-cache-dir & pause")

    def pip_uninstall():
        top.title("用pip卸载" + message.get())
        system("pip uninstall " + message.get() + " --no-cache-dir & pause")

    def pip_install_uninstall():
        system("pip uninstall " + message.get() + " -y & pip install " +
               message.get() + " --no-cache-dir & pause")
        top.title("用pip重新安装" + message.get())

    def show_all_packages():
        system(
            "pip list & --no-cache-dir & echo ------------------------------------------ & pause"
        )
        top.title("显示安装的所有第三方包")

    def show_upgrade_all_packages():
        system(
            "pip list -o & --no-cache-dir & echo ------------------------------------------ & pause"
        )
        top.title("显示能够更新的所有第三方包")

    def upgrade_all_packages():
        system("pip-review --auto & pause")
        top.title("更新所有第三方包")

    def upgrade_packages():
        system("pip-review --local --interactive & pause")
        top.title("更新第三方包")

    def pip_show():
        system("pip show " + message.get() + " --no-cache-dir & pause")
        top.title(message.get())

    def pip_search():
        system("pip search " + message.get() + " --no-cache-dir & pause")
        top.title(message.get())

    def pip_check():
        system("pip check " + message.get() + " --no-cache-dir & pause")
        top.title(message.get())

    def pip_download():
        system("pip download " + message.get() + " --no-cache-dir & pause")
        top.title("用pip下载" + message.get())

    def start():
        with popen("python 邢栋的集成开发环境.pyw") as _:
            print(_.read())

    def python_run():
        system("python " + message.get() + "& echo ------------------ & pause")
        top.title("用python运行" + message.get())

    def c_compile():
        system("gcc -O3 " + message.get() +
               "& echo ------------------ & pause")
        top.title("编译优化" + message.get())

    def run():
        system(message.get())
        top.title("运行" + message.get())

    def java_compile():
        system("javac " + message.get() + "& echo ------------------ & pause")
        top.title("java编译" + message.get())

    def java_run():
        system("java " + message.get() + "& echo ------------------ & pause")
        top.title("java运行" + message.get())

    def dos():
        system("cmd")

    def python():
        system("python")

    def ipython():
        system("ipython")

    def pyinstaller_exe_c():
        system("pyinstaller -F " + message.get() + "& pause")
        top.title(message.get())

    def pyinstaller_exe_w():
        system("pyinstaller -F -w " + message.get() + "& pause")
        top.title(message.get())

    def liulanqi():
        import wx
        from wx.html2 import WebView

        class MAIN(wx.Frame):

            def __init__(self, parent, title):
                wx.Frame.__init__(self, parent, -1, title, size=(1000, 800))
                WebView.New(self).LoadURL(message.get())

        app = wx.App()
        frm = MAIN(None, "浏览" + message.get())
        frm.Show()
        app.MainLoop()

    def calc():
        with popen("calc") as _:
            print(_.read())

    def slidetoshutdown():
        with popen("slidetoshutdown") as _:
            print(_.read())

    def pythonsetuptools():
        system("python setup.py " + message.get())
        top.title("python用setuptools打包" + message.get())

    def vtenv():
        system("python -m venv " + message.get())
        top.title("python用venv创建虚拟环境" + message.get())

    def hack_ping():
        system("ping -l 65500 " + message.get() + " -t & pause")
        top.title("目标IP:" + message.get())

    def ipython_run():
        system("ipython " + message.get() +
               "& echo ------------------ & pause")
        top.title("用ipython运行" + message.get())

    def psl():
        system("powershell")

    def c_compile_run():
        system("gcc -O3 " + message.get() + "& a & pause")
        top.title("编译运行c程序" + message.get())

    def java_compile_run():
        system("javac " + message.get() + "& java " + message.get() +
               ".class" + "& pause")
        top.title("编译运行java程序" + message.get())

    def c_i():
        system("gcc -O3 -E " + message.get() + " -o a.i")
        top.title(message.get())

    def c_s_intel():
        system("gcc -O3 -S -masm=intel " + message.get() + " -o a.s")
        top.title("把" + message.get() + "编译成intel的汇编语言")

    def rm():
        from os import remove
        remove(message.get())
        top.title("已永久删除" + message.get())

    def remv():
        top.title("删除" + message.get())
        shell.SHFileOperation((0, shellcon.FO_DELETE, message.get(), None,
                               shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO
                               | shellcon.FOF_NOCONFIRMATION, None, None))

    def import_colors():
        with popen("python colors.pyw") as _:
            print(_.read())
        top.title("颜色表")

    def pyttsx3_say_messages():
        import pyttsx3
        e = pyttsx3.init()
        e.say(contents.get('1.0', END))
        e.runAndWait()
        top.title("读出文字")

    def pcs():
        system("pycodestyle " + message.get() + "& pause")
        top.title(message.get())

    def labl():
        lbl = Label(text=message.get())
        lbl.pack(side=LEFT)

    def import_fanyi():
        with popen("python youdaofanyi.pyw") as _:
            print(_.read())
        top.title("有道翻译器")

    def pydoc1():
        top.title("python第三方包文档")
        system("python -m pydoc " + message.get() + "& pause")

    def pydoc3():
        top.title("python第三方包文档")
        if message.get() == '':
            system("python -m pydoc -p 80 & pause")
        else:
            system("python -m pydoc -p " + message.get() + "& pause")

    def len_pyttsx3_message():
        import pyttsx3
        f = pyttsx3.init()
        f.say(str(len(contents.get('1.0', END))) + "字")
        f.runAndWait()
        top.title("读出文件字数")

    def tit():
        top.title(message.get())

    def pdb_debug():
        top.title("调试")
        system("python -m pdb " + message.get() + " & pause")

    def ipdb_debug():
        top.title("调试")
        system("python -m ipdb " + message.get() + " & pause")

    def pythoni():
        top.title("运行python程序后运行交互式python")
        system("python -i " + message.get())

    def hide():
        with popen("attrib +H " + message.get()) as _:
            print(_.read())

    def unhide():
        with popen("attrib -H " + message.get()) as _:
            print(_.read())

    def serv():
        system("server")

    def speed():
        system("py -m cProfile " + message.get() + "& pause")

    def dirdir():
        with popen("python dirr.pyw") as _:
            print(_.read())

    def yapfyapf():
        system("yapf -i " + message.get())

    def requirement_install():
        system("pip install -r requirement.txt & pause")

    def pt_python():
        system("ptpython")

    def pt_ipython():
        system("ptipython")

    def read_only():
        top.title("只读" + message.get())
        system("attrib +R " + message.get())

    def not_read_only():
        top.title("解除只读文件" + message.get())
        system("attrib -R " + message.get())

    def python_version():
        from platform import python_version
        messagebox.showinfo("python版本", python_version())
        top.title("python版本")

    def pyttsx3_file_byte():
        top.title("读出字节数")
        import pyttsx3
        import os
        eee = pyttsx3.init()
        eee.say("约" + str(os.path.getsize(message.get())) + "字节")
        eee.runAndWait()

    def shutdown():
        system("shutdown /s /t " + message.get())

    def pip_help():
        system("pip help & pause")

    def coverage_run():
        system("coverage run " + message.get() + "& pause")

    def coverage_report():
        system("coverage report -m " + message.get() + "& pause")

    def coverage_html():
        system("coverage html -d report" + "& pause")

    def on_closing():
        if messagebox.askokcancel("退出", "你确定要退出吗？不要忘了保存！"):
            top.destroy()

    def TREE():
        with popen("python tre.pyw") as _:
            print(_.read())

    def process_key(key):
        current_line_num, current_col_num = map(
            int,
            contents.index(INSERT).split('.'))
        if key.keycode == 13:
            last_line_num = current_line_num - 1
            last_line = contents.get(f'{last_line_num}.0', INSERT).rstrip()
            num = len(last_line) - len(last_line.lstrip(' '))
            if (last_line.endswith(':')
                    or (':' in last_line
                        and last_line.split(':')[-1].strip().stratswit('#'))):
                num += 4
            elif last_line.strip().startswith(
                ('return', 'break', 'continue', 'pass', 'raise')):
                num -= 4
            contents.insert(INSERT, ' ' * num)
        elif key.keysym == 'Backspace':
            current_line = contents.get(
                f'{current_line_num}.0',
                f'{current_line_num}.{current_col_num}')
            num = len(current_line) - len(current_line.rstrip(' '))
            num = min(3, num)
            if num > 1:
                contents.delete(f'{current_line_num}.{current_col_num-num}',
                                f'{current_line_num}.{current_col_num}')
        else:
            lines = contents.get('0.0',
                                 END).rstrip('\n').splitlines(keepends=True)
            contents.delete('0.0', END)
            for line in lines:
                flag1, flag2, flag3 = False, False, False
                for index, ch in enumerate(line):
                    if ch == "'" and not flag2:
                        flag3 = not flag3
                        contents.insert(INSERT, ch, 'string')
                    elif ch == '"' and not flag3:
                        flag2 = not flag2
                        contents.insert(INSERT, ch, 'string')
                    elif flag2 or flag3:
                        contents.insert(INSERT, ch, 'string')
                    else:
                        if ch not in string.ascii_letters:
                            if flag1:
                                flag1 = False
                                word = line[start:index]
                                if word in bifs:
                                    contents.insert(INSERT, word, 'bif')
                                elif word in kws:
                                    contents.insert(INSERT, word, 'kw')
                                else:
                                    contents.insert(INSERT, word)
                            if ch == '#':
                                contents.insert(INSERT, line[index:],
                                                'comment')
                                break
                            else:
                                contents.insert(INSERT, ch)
                        else:
                            if not flag1:
                                flag1 = True
                                start = index
                if flag1:
                    flag1 = False
                    word = line[start:]
                    if word in bifs:
                        contents.insert(INSERT, word, 'bif')
                    elif word in kws:
                        contents.insert(INSERT, word, 'kw')
                    else:
                        contents.insert(INSERT, word)
            contents.mark_set('insert',
                              f'{current_line_num}.{current_col_num}')

    def other_theme():
        contents.bind('<KeyRelease>', process_key)
        contents.tag_config('bif', foreground='red')
        contents.tag_config('kw', foreground='darkblue')
        contents.tag_config('comment', foreground='gray')
        contents.tag_config('string', foreground='darkgreen')

    def normal_theme():
        contents.bind('<KeyRelease>', process_key)
        contents.tag_config('bif', foreground='tomato')
        contents.tag_config('kw', foreground='deepskyblue')
        contents.tag_config('comment', foreground='purple')
        contents.tag_config('string', foreground='green')

    def third_theme():
        contents.bind('<KeyRelease>', process_key)
        contents.tag_config('bif', foreground='deepskyblue')
        contents.tag_config('kw', foreground='tomato')
        contents.tag_config('comment', foreground='gray')
        contents.tag_config('string', foreground='darkgoldenrod')

    def fourth_theme():
        contents.bind('<KeyRelease>', process_key)
        contents.tag_config('bif', foreground='purple')
        contents.tag_config('kw', foreground='purple')
        contents.tag_config('comment', foreground='gray')
        contents.tag_config('string', foreground='green')

    def go_run():
        system("go run " + message.get())
        top.title("运行go程序")

    def go_build():
        system("go build " + message.get())
        top.title("把go程序编译成exe文件")

    class MyThread(Thread):

        def __init__(self, func, *args):
            super().__init__()
            self.func = func
            self.args = args
            self.setDaemon(True)
            self.start()

        def run(self):
            self.func(*self.args)

    def git_init():
        system("git init & pause")
        top.title("git init")

    def git_add():
        system("git add " + message.get() + " & pause")
        top.title("git add")

    def git_commit():
        system('git commit -m "%s" & pause' % (message.get()))
        top.title("git commit")

    def git_diff():
        system("git diff & pause")
        top.title("git diff")

    def git_clone():
        system("git clone " + message.get() + " & pause")
        top.title("git clone")

    def bpython():
        system("bpython")

    def mypy_type():
        system("mypy " + message.get())

    def pyenv_install():
        system("pyenv install " + message.get())

    def pyenv_uninstall():
        system("pyenv uninstall " + message.get())

    def pyenv_update():
        system("pyenv update " + message.get())

    def pythonorg():
        from webbrowser import open
        open("https://www.python.org/")

    def baidu():
        from webbrowser import open
        open(f"https://www.baidu.com/s?wd={message.get()}&ie=utf-8")

    def pyenv_list():
        system("pyenv install -l")

    bifs = dir(__builtins__)
    kws = kwlist
    top = Tk()
    top.title("我的集成开发环境(作者：邢栋)")
    top.geometry('1520x700')
    hook_dropfiles(top, func=dragged_load)
    menubar = Menu(top)
    contents = ScrolledText(font=40)
    contents.pack(side=BOTTOM, expand=True, fill=BOTH)
    top.protocol("WM_DELETE_WINDOW", on_closing)
    contents.bind('<KeyRelease>', process_key)
    contents.tag_config('bif', foreground='tomato')
    contents.tag_config('kw', foreground='deepskyblue')
    contents.tag_config('comment', foreground='purple')
    contents.tag_config('string', foreground='green')
    Label(text=getcwd(), fg='red').pack(side=LEFT)
    message = Entry(font=40)
    message.pack(side=LEFT, expand=True, fill=X)
    menu1 = Menu(menubar, tearoff=False)
    menu1.add_command(label='打开文件', command=lambda: MyThread(load))
    menu1.add_command(label='保存文件', command=lambda: MyThread(save))
    menu1.add_command(label='隐藏文件', command=hide)
    menu1.add_command(label='恢复隐藏的文件', command=unhide)
    menu1.add_command(label='只读文件', command=read_only)
    menu1.add_command(label='解除只读文件', command=not_read_only)
    menu1.add_command(label='读出字节数', command=pyttsx3_file_byte)
    menu1.add_command(label='创建文件夹', command=md)
    menu1.add_command(label='删除文件夹', command=rd)
    menu1.add_command(label='创建递归文件夹', command=mds)
    menu1.add_command(label='删除递归文件夹', command=rds)
    menu1.add_command(label='清理python缓存', command=python_cache)
    menu1.add_command(label='以命令行的python格式保存文件(.py)', command=python_save)
    menu1.add_command(label='以可视化的python格式保存文件(.pyw)', command=pythonw_save)
    menu1.add_command(label='以c语言的格式保存(.c)', command=c_save)
    menu1.add_command(label='以c++语言的格式保存(.cpp)', command=cpp_save)
    menu1.add_command(label='以java语言的格式保存(.java)', command=java_save)
    menu1.add_command(label='以html的格式保存(.htm)', command=html_save)
    menu1.add_command(label='以c语言头文件的格式保存(.h)', command=h_save)
    menu1.add_command(label='以批处理文件的格式保存(.bat)', command=bat_save)
    menu1.add_command(label='删除文件', command=remv)
    menu1.add_command(label='永久删除文件', command=rm)
    menubar.add_cascade(label="文本编辑", menu=menu1)
    top.config(menu=menubar)
    menu2 = Menu(menubar, tearoff=False)
    menu2.add_command(label='提供可选项更新第三方包',
                      command=lambda: MyThread(upgrade_packages))
    menu2.add_command(label='更新所有第三方包',
                      command=lambda: MyThread(upgrade_all_packages))
    menu2.add_command(label='显示能够更新的所有第三方包',
                      command=lambda: MyThread(show_upgrade_all_packages))
    menu2.add_command(label='显示安装的所有第三方包',
                      command=lambda: MyThread(show_all_packages))
    menu2.add_command(label='pip帮助', command=pip_help)
    menu2.add_command(label='检查依赖', command=pip_check)
    menu2.add_command(label='搜索', command=pip_search)
    menu2.add_command(label='查看信息', command=pip_show)
    menu2.add_command(label='用requirement.txt中的包安装',
                      command=lambda: MyThread(requirement_install))
    menu2.add_command(label='下载安装包', command=lambda: MyThread(pip_download))
    menu2.add_command(label='卸载', command=pip_uninstall)
    menu2.add_command(label='重新安装',
                      command=lambda: MyThread(pip_install_uninstall))
    menu2.add_command(label='升级', command=lambda: MyThread(pip_upgrade))
    menu2.add_command(label='安装', command=lambda: MyThread(pip_install))
    menubar.add_cascade(label="python第三方包软件商店", menu=menu2)
    top.config(menu=menubar)
    menu3 = Menu(menubar, tearoff=False)
    menu3.add_command(label='运行python程序', command=python_run)
    menu3.add_command(label='用ipython运行python程序', command=ipython_run)
    menu3.add_command(label='运行python程序后运行交互式python', command=pythoni)
    menu3.add_command(label='编译c程序', command=c_compile)
    menu3.add_command(label='预处理c程序', command=c_i)
    menu3.add_command(label='编译c程序成汇编语言', command=c_s_intel)
    menu3.add_command(label='运行.exe或.bat程序', command=run)
    menu3.add_command(label='编译运行c程序', command=c_compile_run)
    menu3.add_command(label='运行go程序', command=go_run)
    menu3.add_command(label='把go程序编译成exe文件', command=go_build)
    menu3.add_command(label='编译java程序', command=java_compile)
    menu3.add_command(label='运行java程序', command=java_run)
    menu3.add_command(label='编译运行java程序', command=java_compile_run)
    menubar.add_cascade(label="编译与运行", menu=menu3)
    top.config(menu=menubar)
    menu4 = Menu(menubar, tearoff=False)
    menu4.add_command(label='dos', command=lambda: MyThread(dos))
    menu4.add_command(label='python', command=lambda: MyThread(python))
    menu4.add_command(label='ipython', command=lambda: MyThread(ipython))
    menu4.add_command(label='ptpython', command=lambda: MyThread(pt_python))
    menu4.add_command(label='ptipython', command=lambda: MyThread(pt_ipython))
    menu4.add_command(label='bpython', command=lambda: MyThread(bpython))
    menu4.add_command(label='powershell', command=lambda: MyThread(psl))
    menubar.add_cascade(label="命令行", menu=menu4)
    top.config(menu=menubar)
    menu5 = Menu(menubar, tearoff=False)
    menu5.add_command(label='把python程序编译成命令行的exe',
                      command=lambda: MyThread(pyinstaller_exe_c))
    menu5.add_command(label='把python程序编译成可视化的exe',
                      command=lambda: MyThread(pyinstaller_exe_w))
    menubar.add_cascade(label="把python程序编译成exe", menu=menu5)
    top.config(menu=menubar)
    menu6 = Menu(menubar, tearoff=False)
    menu6.add_command(label='命令行', command=pydoc1)
    menu6.add_command(label='所有第三方包的网页版', command=pydoc3)
    menubar.add_cascade(label="第三方包文档", menu=menu6)
    top.config(menu=menubar)
    menu7 = Menu(menubar, tearoff=False)
    menu7.add_command(label='读出文字', command=pyttsx3_say_messages)
    menu7.add_command(label='读出文件字数', command=len_pyttsx3_message)
    menubar.add_cascade(label='朗读', menu=menu7)
    top.config(menu=menubar)
    menu8 = Menu(menubar, tearoff=False)
    menu8.add_command(label='显示运行速度', command=speed)
    menu8.add_command(label='用pdb调试', command=lambda: MyThread(pdb_debug))
    menu8.add_command(label='用ipdb调试', command=lambda: MyThread(ipdb_debug))
    menubar.add_cascade(label='python调试', menu=menu8)
    top.config(menu=menubar)
    menu9 = Menu(menubar, tearoff=False)
    menu9.add_command(label='修改为1号风格（默认）', command=normal_theme)
    menu9.add_command(label='修改为2号风格', command=other_theme)
    menu9.add_command(label='修改为3号风格', command=third_theme)
    menu9.add_command(label='修改为4号风格', command=fourth_theme)
    menubar.add_cascade(label='语法高亮风格', menu=menu9)
    top.config(menu=menubar)
    menu10 = Menu(menubar, tearoff=False)
    menu10.add_command(label='显示目录下的文件', command=lambda: MyThread(dirdir))
    menu10.add_command(label='显示目录结构', command=lambda: MyThread(TREE))
    menubar.add_cascade(label='显示目录', menu=menu10)
    top.config(menu=menubar)
    menu11 = Menu(menubar, tearoff=False)
    menu11.add_command(label='检查python程序规范', command=pcs)
    menu11.add_command(label='把python代码修改成规范的样子', command=yapfyapf)
    menubar.add_cascade(label='python代码规范', menu=menu11)
    top.config(menu=menubar)
    menu12 = Menu(menubar, tearoff=False)
    menu12.add_command(label='滑动关机', command=slidetoshutdown)
    menu12.add_command(label='定时关机', command=shutdown)
    menubar.add_cascade(label='关机', menu=menu12)
    top.config(menu=menubar)
    menu13 = Menu(menubar, tearoff=False)
    menu13.add_command(label='生成测试文件并运行', command=coverage_run)
    menu13.add_command(label='显示结果', command=coverage_report)
    menu13.add_command(label='生成html文件夹', command=coverage_html)
    menubar.add_cascade(label='python测试覆盖率', menu=menu13)
    top.config(menu=menubar)
    menu14 = Menu(menubar, tearoff=False)
    menu14.add_command(label='init', command=git_init)
    menu14.add_command(label='add', command=git_add)
    menu14.add_command(label='clone', command=git_clone)
    menu14.add_command(label='commit', command=git_commit)
    menu14.add_command(label='diff', command=git_diff)
    menubar.add_cascade(label='git', menu=menu14)
    top.config(menu=menubar)
    menu15 = Menu(menubar, tearoff=False)
    menu15.add_command(label='安装', command=lambda: MyThread(pyenv_install))
    menu15.add_command(label='卸载', command=lambda: MyThread(pyenv_uninstall))
    menu15.add_command(label='更新', command=lambda: MyThread(pyenv_update))
    menu15.add_command(label='能安装的目录', command=lambda: MyThread(pyenv_list))
    menubar.add_cascade(label='pyenv', menu=menu15)
    top.config(menu=menubar)
    Button(text='再启动一个窗口', command=lambda: MyThread(start)).pack(side=RIGHT)
    Button(text='浏览器', command=lambda: MyThread(liulanqi)).pack(side=RIGHT)
    Button(text='计算器', command=lambda: MyThread(calc)).pack(side=RIGHT)
    Button(text='添加到任务栏', command=labl).pack(side=RIGHT)
    Button(text='死亡之ping',
           command=lambda: MyThread(hack_ping)).pack(side=RIGHT)
    Button(text='有道翻译器',
           command=lambda: MyThread(import_fanyi)).pack(side=RIGHT)
    Button(text='创建虚拟环境', command=lambda: MyThread(vtenv)).pack(side=RIGHT)
    Button(text='用setuptools打包(需先填写setup.py)',
           command=lambda: MyThread(pythonsetuptools)).pack(side=RIGHT)
    Button(text='颜色表',
           command=lambda: MyThread(import_colors)).pack(side=RIGHT)
    Button(text='修改标题', command=tit)
    Button(text='启动80端口服务器', command=lambda: MyThread(serv)).pack(side=RIGHT)
    Button(text='类型检查', command=lambda: MyThread(mypy_type)).pack(side=RIGHT)
    Button(text='百度', command=lambda: MyThread(baidu)).pack(side=RIGHT)
    Button(text='python官网',
           command=lambda: MyThread(pythonorg)).pack(side=RIGHT)
    Button(text='python版本',
           command=lambda: MyThread(python_version)).pack(side=LEFT)
    mainloop()
except Exception as e:
    print(e)
