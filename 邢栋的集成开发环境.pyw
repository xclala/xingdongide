try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from subprocess import PIPE
    from subprocess import run as run_cmd
    from string import ascii_letters
    from keyword import kwlist
    from threading import Thread
    from sys import executable
    from os import name as osname
    from os.path import abspath
    from platform import python_version_tuple, python_version

    opened_file_path = ""

    class MyThread(Thread):

        def __init__(self, func, *args):
            super().__init__()
            self.func = func
            self.args = args
            self.daemon = True
            self.start()

        def run(self):
            self.func(*self.args)

    def terminal_output(output):
        root = Tk()
        root.title("")
        root.state("zoomed")
        root.resizable(0, 0)
        contents = ScrolledText(root, font=40)
        contents.pack(side=BOTTOM, expand=True, fill=BOTH)
        contents.delete('1.0', END)
        contents.insert(INSERT, output)
        mainloop()

    def hook_dropfiles(tkwindow_or_winfoid, func, force_unicode=False):
        if osname == 'nt':
            import ctypes

            hwnd = tkwindow_or_winfoid.winfo_id()\
                if getattr(tkwindow_or_winfoid, "winfo_id", None)\
                else tkwindow_or_winfoid

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
                    raise "over hook limit number 200, to protect the computer."
                if "old_wndproc_%d" % i not in globals():
                    old, new = "old_wndproc_%d" % i, "new_wndproc_%d" % i
                    break

            globals()[old] = None
            globals()[new] = prototype(py_drop_func)

            ctypes.windll.shell32.DragAcceptFiles(hwnd, True)
            globals()[old] = GetWindowLong(hwnd, GWL_WNDPROC)
            SetWindowLong(hwnd, GWL_WNDPROC, globals()[new])

    def load():
        global opened_file_path
        opened_file_path = askopenfilename(title="打开文件")
        with open(opened_file_path, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title(f"打开{opened_file_path}")

    def dragged_load(files):
        global opened_file_path
        opened_file_path = files[0].decode("gbk")
        with open(opened_file_path, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title(f"打开{opened_file_path}")

    def save(resave=False):
        global opened_file_path
        if not opened_file_path:
            opened_file_path = asksaveasfilename(title="另存为文件")
            resave = True
        if resave:
            opened_file_path = asksaveasfilename(title="另存为文件")
        with open(opened_file_path, 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title(f"已保存{opened_file_path}")

    def md():
        from os import mkdir
        mkdir(message.get())

    def rd():
        from os import rmdir
        rmdir(message.get())

    def pip(arg):
        top.title("pip")
        base = [executable, '-m', 'pip', arg, message.get()]
        if arg == 'upgrade':
            base[3] = 'install'
            base.insert(4, '--upgrade')
        if arg == 'requirements_install':
            base[3] = 'install'
            base.insert(4, '-r')
            base.insert(5, 'requirements.txt')
        o = run_cmd(base, shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        messagebox.showinfo("运行完成", "运行完成")
        top.title("邢栋的集成开发环境")

    def pip_reinstall():
        pip("uninstall")
        pip("install")
        top.title("邢栋的集成开发环境")

    def upgrade_all_packages():
        top.title("正在更新所有第三方包")
        from json import loads
        a = run_cmd(
            [executable, "-m", "pip", "list", "--outdated", "--format=json"],
            stdout=PIPE,
            shell=True)
        for i in loads(a.stdout.decode()):
            o = run_cmd(
                [executable, "-m", "pip", "install", "--upgrade", i["name"]],
                shell=True,
                stdout=PIPE)
        terminal_output(o.stdout.decode())
        messagebox.showinfo("更新完成", "更新完成")
        top.title("邢栋的集成开发环境")

    def python_run():
        global opened_file_path
        o = run_cmd([executable, opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"用python运行{opened_file_path}")

    def c_compile():
        global opened_file_path
        o = run_cmd(["gcc", "-O3", opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"编译优化{opened_file_path}")

    def java_compile():
        global opened_file_path
        o = run_cmd(["javac", opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"java编译{opened_file_path}")

    def java_run():
        global opened_file_path
        o = run_cmd(["java", opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"java运行{opened_file_path}")

    def pyinstaller_exe(window):
        global opened_file_path
        base = ["pyinstaller", "-F", opened_file_path]
        if window:
            _ = base.insert(2, '-w')
        top.title(f"正在用pyinstaller打包{opened_file_path}")
        o = run_cmd(base, shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title("邢栋的集成开发环境")
        messagebox.showinfo("打包完成", "打包完成")

    def vtenv():
        t = message.get()
        top.title(f"正在用venv创建虚拟环境{t}")
        if t == '':
            t = '.'
        run_cmd([executable, "-m", "venv", t], shell=True)
        top.title("邢栋的集成开发环境")
        messagebox.showinfo("成功用venv创建虚拟环境", "成功用venv创建虚拟环境")

    def hack_ping():
        if osname == "nt":
            top.title("正在攻击:" + message.get())
            run_cmd(['ping', '-l', '65500', message.get(), '-t'], shell=True)

    def c_compile_run():
        global opened_file_path
        o = run_cmd(
            ['gcc', '-O3', opened_file_path, '-o', 'a.exe', '&', "a.exe"],
            shell=True,
            stdout=True)
        terminal_output(o.stdout.decode())
        top.title(f"编译运行c程序{opened_file_path}")

    def java_compile_run():
        global opened_file_path
        o = run_cmd(['javac', opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        o = run_cmd(['java', f"{opened_file_path}.class"],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"编译运行java程序{opened_file_path}")

    def c_i():
        global opened_file_path
        o = run_cmd(['gcc', '-O3', '-E', opened_file_path, "-o", "a.i"],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(opened_file_path)

    def c_s():
        global opened_file_path
        o = run_cmd(['gcc', '-O3', '-S', opened_file_path, "-o", "a.i"],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title(f"把{opened_file_path}编译成汇编语言")

    def rm():
        global opened_file_path
        from os import remove
        remove(opened_file_path)
        top.title(f"已永久删除{opened_file_path}")

    def remv():
        if osname == 'nt':
            from win32com.shell import shell, shellcon
            global opened_file_path
            top.title(f"删除{opened_file_path}")
            shell.SHFileOperation(
                (0, shellcon.FO_DELETE, opened_file_path, None,
                 shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO
                 | shellcon.FOF_NOCONFIRMATION, None, None))

    def colours():
        top.title("颜色表")
        with open("colors", encoding="utf-8") as temp:
            colors = temp.read()
        root = Tk()
        root.title("颜色表")
        root.geometry('1230x650')
        root.resizable(0, 0)
        i = 0
        colcut = 5
        for color in colors.split("\n"):
            sp = color.split(' ')
            Label(root, text=color, bg=sp[1]).grid(row=int(i / colcut),
                                                   column=i % colcut,
                                                   sticky=W + E + N + S)
            i += 1
        root.mainloop()

    def pydoc1():
        top.title("python第三方包文档")
        o = run_cmd([executable, '-m', 'pydoc',
                     message.get()],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def pydoc3():
        top.title("python第三方包文档")
        if message.get() == '':
            port = 80
        o = run_cmd([executable, '-m', 'pydoc', '-p',
                     message.get()],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def tit():
        top.title(message.get())

    def speed():
        global opened_file_path
        o = run_cmd([executable, '-m', 'cProfile', opened_file_path],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def dirdir():
        from os import scandir
        _ = []
        for item in scandir('.'):
            _.append(item.path)
        terminal_output(_)

    def yapfyapf():
        from yapf.yapflib.yapf_api import FormatFile
        global opened_file_path
        FormatFile(opened_file_path, in_place=True)
        with open(opened_file_path, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())

    def Replace():

        def replace_text():
            temp = contents.get('1.0', END)
            contents.delete('1.0', END)
            contents.insert(INSERT, temp.replace(m.get(), r.get()))
            save()
            root.destroy()

        root = Tk()
        root.title("替换")
        root.geometry("200x150")
        root.resizable(0, 0)
        Label(root, text="原文字：").pack()
        m = Entry(root)
        m.pack()
        Label(root, text="替换成：").pack()
        r = Entry(root)
        r.pack()
        Button(root, text="确定", command=replace_text).pack(side=BOTTOM)
        mainloop()

    def alert_file_byte():
        global opened_file_path
        from os.path import getsize
        top.title("显示字节数")
        messagebox.showinfo("约" + str(getsize(opened_file_path)) + "字节",
                            "约" + str(getsize(opened_file_path)) + "字节")

    def coverage_run():
        global opened_file_path
        o = run_cmd(['coverage', 'run', opened_file_path],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def coverage_report():
        global opened_file_path
        o = run_cmd(['coverage', 'report', "-m", opened_file_path],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def coverage_html():
        global opened_file_path
        o = run_cmd(['coverage', 'html', "-d", "report"],
                    shell=True,
                    stdout=PIPE)
        terminal_output(o.stdout.decode())

    def on_closing():
        if contents.get('1.0', END).strip():
            if messagebox.askyesno(top, message="你要保存吗？"):
                save()
        top.destroy()

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
                        if ch not in ascii_letters:
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
        global opened_file_path
        o = run_cmd(['go', 'run', opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title("运行go程序")

    def go_build():
        global opened_file_path
        o = run_cmd(['go', 'build', opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title("把go程序编译成exe文件")

    def git_init():
        run_cmd(['git', 'init'], shell=True, stdout=PIPE)
        top.title("git init")

    def git_add():
        t = message.get()
        if t == '':
            t = '.'
        run_cmd(['git', 'add', t], shell=True, stdout=PIPE)
        top.title("git add")

    def git_commit():
        run_cmd(['git', 'commit', "-m", message.get()],
                shell=True,
                stdout=PIPE)
        top.title("git commit")

    def git_diff():
        o = run_cmd(['git', 'diff'], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())
        top.title("git diff")

    def git_clone():
        top.title("git clone")
        run_cmd(['git', 'clone', message.get()], shell=True, stdout=PIPE)
        top.title("邢栋的集成开发环境")

    def mypy_type():
        global opened_file_path
        o = run_cmd(['mypy', opened_file_path], shell=True, stdout=PIPE)
        terminal_output(o.stdout.decode())

    def pythonorg():
        from webbrowser import open
        open("https://www.python.org/")

    def baidu():
        from webbrowser import open
        open(f"https://www.baidu.com/s?wd={message.get()}&ie=utf-8")

    def on_key_release(event):
        if opened_file_path:
            save()
        process_key(event)

    bifs = dir(__builtins__)
    kws = kwlist
    top = Tk()
    top.title("邢栋的集成开发环境")
    top.state("zoomed")
    top.protocol("WM_DELETE_WINDOW", on_closing)
    hook_dropfiles(top, func=dragged_load)
    contents = ScrolledText(font=40)
    contents.pack(side=BOTTOM, expand=True, fill=BOTH)
    contents.bind('<KeyRelease>', on_key_release)
    contents.bind('<Control-o>', lambda event: load())
    contents.bind('<Control-S>',
                  lambda event: save(resave=True))  #Ctrl+Shift+s
    contents.bind('<Control-N>', lambda event: MyThread(
        run_cmd, [executable, abspath(__file__)], True))  #Ctrl+Shift+n
    contents.tag_config('bif', foreground='tomato')
    contents.tag_config('kw', foreground='deepskyblue')
    contents.tag_config('comment', foreground='purple')
    contents.tag_config('string', foreground='green')
    Label(text=f"Python {python_version()}", fg='red').pack(side=LEFT)
    message = Entry(font=40)
    message.pack(side=LEFT, expand=True, fill=X)
    menubar = Menu(top)
    menu1 = Menu(menubar, tearoff=False)
    menu1.add_command(label='打开文件', command=load)
    menu1.add_command(label='保存文件', command=save)
    menu1.add_command(label='另存为文件', command=lambda: save(resave=True))
    menu1.add_command(label='隐藏文件',
                      command=run_cmd(
                          ["attrib", "+H", message.get()], shell=True))
    menu1.add_command(label='恢复隐藏的文件',
                      command=run_cmd(
                          ["attrib", "-H", message.get()], shell=True))
    menu1.add_command(label='只读文件',
                      command=run_cmd(
                          ["attrib", "+R", message.get()], shell=True))
    menu1.add_command(label='解除只读文件',
                      command=run_cmd(
                          ["attrib", "-R", message.get()], shell=True))
    menu1.add_command(label='显示字节数', command=alert_file_byte)
    menu1.add_command(label='创建文件夹', command=md)
    menu1.add_command(label='删除文件夹', command=rd)
    if osname == 'nt':
        menu1.add_command(label='删除文件', command=remv)
    menu1.add_command(label='永久删除文件', command=rm)
    menubar.add_cascade(label="文件管理", menu=menu1)
    top.config(menu=menubar)
    menu2 = Menu(menubar, tearoff=False)
    menu2.add_command(label='更新所有第三方包',
                      command=lambda: MyThread(upgrade_all_packages))
    menu2.add_command(label='检查依赖', command=lambda: pip("check"))
    menu2.add_command(label='搜索', command=lambda: pip("search"))
    menu2.add_command(label='查看信息', command=lambda: pip("show"))
    menu2.add_command(label='安装requirements.txt中的包',
                      command=lambda: pip("requirements_install"))
    menu2.add_command(label='显示所有安装的包', command=lambda: pip("list"))
    menu2.add_command(label='下载安装包', command=lambda: pip("download"))
    menu2.add_command(label='卸载', command=lambda: pip("uninstall"))
    menu2.add_command(label='重新安装', command=lambda: MyThread(pip_reinstall))
    menu2.add_command(label='升级', command=lambda: pip("upgrade"))
    menu2.add_command(label='安装', command=lambda: pip("install"))
    menubar.add_cascade(label="python第三方包管理器", menu=menu2)
    top.config(menu=menubar)
    menu3 = Menu(menubar, tearoff=False)
    menu3.add_command(label='运行python程序', command=python_run)
    menu3.add_command(label='把python程序编译成命令行的exe',
                      command=lambda: pyinstaller_exe(False))
    menu3.add_command(label='把python程序编译成可视化的exe',
                      command=lambda: pyinstaller_exe(True))
    menu3.add_command(label='编译c程序', command=c_compile)
    menu3.add_command(label='预处理c程序', command=c_i)
    menu3.add_command(label='编译c程序成汇编语言', command=c_s)
    menu3.add_command(label='编译运行c程序', command=c_compile_run)
    menu3.add_command(label='运行go程序', command=go_run)
    menu3.add_command(label='把go程序编译成exe文件',
                      command=go_build)
    menu3.add_command(label='编译java程序', command=java_compile)
    menu3.add_command(label='运行java程序', command=java_run)
    menu3.add_command(label='编译运行java程序',
                      command=java_compile_run)
    menubar.add_cascade(label="编译与运行", menu=menu3)
    top.config(menu=menubar)
    menu4 = Menu(menubar, tearoff=False)
    menu4.add_command(label='cmd',
                      command=lambda: MyThread(run_cmd, "cmd", True))
    menu4.add_command(label='powershell',
                      command=lambda: MyThread(run_cmd, "powershell", True))
    menubar.add_cascade(label="命令行", menu=menu4)
    top.config(menu=menubar)
    menu5 = Menu(menubar, tearoff=False)
    menu5.add_command(label='命令行', command=lambda: MyThread(pydoc1))
    menu5.add_command(label='所有第三方包的网页版', command=lambda: MyThread(pydoc3))
    menubar.add_cascade(label="第三方包文档", menu=menu5)
    top.config(menu=menubar)
    menu6 = Menu(menubar, tearoff=False)
    menu6.add_command(label='修改为1号风格（默认）', command=normal_theme)
    menu6.add_command(label='修改为2号风格', command=other_theme)
    menu6.add_command(label='修改为3号风格', command=third_theme)
    menu6.add_command(label='修改为4号风格', command=fourth_theme)
    menubar.add_cascade(label='语法高亮风格', menu=menu6)
    top.config(menu=menubar)
    menu7 = Menu(menubar, tearoff=False)
    menu7.add_command(label='生成测试文件并运行',
                      command=lambda: MyThread(coverage_run))
    menu7.add_command(label='显示结果', command=lambda: MyThread(coverage_report))
    menu7.add_command(label='生成html文件夹',
                      command=lambda: MyThread(coverage_html))
    menubar.add_cascade(label='python测试覆盖率', menu=menu7)
    top.config(menu=menubar)
    menu8 = Menu(menubar, tearoff=False)
    menu8.add_command(label='init', command=lambda: MyThread(git_init))
    menu8.add_command(label='add', command=lambda: MyThread(git_add))
    menu8.add_command(label='clone', command=lambda: MyThread(git_clone))
    menu8.add_command(label='commit', command=lambda: MyThread(git_commit))
    menu8.add_command(label='diff', command=lambda: MyThread(git_diff))
    menubar.add_cascade(label='git', menu=menu8)
    top.config(menu=menubar)
    Button(
        text='再启动一个窗口',
        command=lambda: MyThread(
            run_cmd, [executable, abspath(__file__)], True)).pack(side=RIGHT)
    Button(text='计算器',
           command=lambda: MyThread(run_cmd, "calc", True)).pack(side=RIGHT)
    if osname == 'nt':
        Button(text='死亡之ping',
               command=lambda: MyThread(hack_ping)).pack(side=RIGHT)
    Button(text="yapf格式化", command=lambda: MyThread(yapfyapf)).pack(side=RIGHT)
    Button(text='创建虚拟环境', command=lambda: MyThread(vtenv)).pack(side=RIGHT)
    Button(text='显示运行速度', command=lambda: MyThread(speed)).pack(side=RIGHT)
    Button(text='颜色表', command=colours).pack(side=RIGHT)
    Button(text='修改标题', command=tit).pack(side=RIGHT)
    Button(text='类型检查', command=lambda: MyThread(mypy_type)).pack(side=RIGHT)
    Button(text='百度', command=lambda: MyThread(baidu)).pack(side=RIGHT)
    Button(text='python官网',
           command=lambda: MyThread(pythonorg)).pack(side=RIGHT)
    Button(text="显示目录文件", command=dirdir).pack(side=RIGHT)
    Button(text="替换", command=Replace).pack(side=RIGHT)
    if python_version_tuple()[0] == '3' and int(python_version_tuple()[1]) > 5:
        mainloop()
except Exception as e:
    print(e)
