try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from os import system, popen
    from subprocess import run, PIPE
    from os.path import abspath
    from string import ascii_letters
    from keyword import kwlist
    from threading import Thread
    opened_file_path = ""

    def hook_dropfiles(tkwindow_or_winfoid, func, force_unicode=False):
        import ctypes
        from ctypes.wintypes import DWORD

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
        global opened_file_path
        opened_file_path = askopenfilename(title="打开文件")
        with open(opened_file_path, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title("打开" + opened_file_path)

    def dragged_load(files):
        global opened_file_path
        opened_file_path = files[0].decode("gbk")
        with open(opened_file_path, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
        top.title("打开" + opened_file_path)

    def save():
        global opened_file_path
        if opened_file_path:
            with open(opened_file_path, 'w', encoding='utf-8') as file:
                file.write(contents.get('1.0', END))
            top.title("已保存" + opened_file_path)
        else:
            resave()


    def resave():
        global opened_file_path
        opened_file_path = asksaveasfilename(title="另存为文件")
        with open(opened_file_path, 'w', encoding='utf-8') as file:
            file.write(contents.get('1.0', END))
        top.title("另存为" + opened_file_path)

    def md():
        from os import mkdir
        mkdir(message.get())

    def rd():
        from os import rmdir
        rmdir(message.get())

    def python_cache():
        from os import removedir
        removedir("__pycache__")

    def pip_install():
        top.title("正在用pip安装" + message.get())
        run(["pip", "install", message.get()], shell=True)
        messagebox.showinfo("安装完成", "安装完成")
        top.title("")

    def pip_upgrade():
        top.title("正在用pip升级" + message.get())
        run(["pip", "install", "--upgrade", message.get()], shell=True)
        messagebox.showinfo("更新完成", "更新完成")
        top.title("")

    def pip_uninstall():
        top.title("正在用pip卸载" + message.get())
        run(["pip", "uninstall", message.get()], shell=True)
        messagebox.showinfo("卸载完成", "卸载完成")
        top.title("")

    def pip_install_uninstall():
        top.title("正在用pip重新安装" + message.get())
        run(["pip", "uninstall", message.get(), "-y"], shell=True)
        run(["pip", "install", message.get()], shell=True)
        messagebox.showinfo("重新安装完成", "重新安装完成")
        top.title("")

    def show_all_packages():
        system("pip list & pause")
        top.title("显示安装的所有第三方包")

    def show_upgrade_all_packages():
        system("pip list --outdated & pause")
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
        top.title("正在用pip下载" + message.get())
        run(["pip", "download", message.get()], shell=True)
        messagebox.showinfo("下载完成", "下载完成")
        top.title("")

    def python_run():
        global opened_file_path
        system("python " + opened_file_path +
                "& echo ------------------ & pause")
        top.title("用python运行" + opened_file_path)

    def c_compile():
        global opened_file_path
        system("gcc -O3 " + opened_file_path +
                "& echo ------------------ & pause")
        top.title("编译优化" + opened_file_path)

    def java_compile():
        global opened_file_path
        system("javac " + opened_file_path +
                "& echo ------------------ & pause")
        top.title("java编译" + opened_file_path)

    def java_run():
        global opened_file_path
        system("java " + opened_file_path +
                "& echo ------------------ & pause")
        top.title("java运行" + opened_file_path)

    def pyinstaller_exe_c():
        global opened_file_path
        top.title("正在用pyinstaller打包命令行" + opened_file_path)
        run(["pyinstaller", "-F", opened_file_path], shell=True)
        top.title("")
        messagebox.showinfo("打包完成", "打包完成")

    def pyinstaller_exe_w():
        global opened_file_path
        top.title("正在用pyinstaller打包可视化" + opened_file_path)
        run(["pyinstaller", "-F", "-w", opened_file_path], shell=True)
        top.title("")
        messagebox.showinfo("打包完成", "打包完成")

    def liulanqi():
        from webbrowser import open
        open(message.get())

    def vtenv():
        top.title("正在用venv创建虚拟环境" + message.get())
        run(["python", "-m", "venv", message.get()], shell=True)
        top.title("")
        messagebox.showinfo("成功用venv创建虚拟环境", "成功用venv创建虚拟环境")

    def hack_ping():
        system("ping -l 65500 " + message.get() + " -t & pause")
        top.title("目标IP:" + message.get())

    def ipython_run():
        global opened_file_path
        system("ipython " + opened_file_path +
                "& echo ------------------ & pause")
        top.title("用ipython运行" + opened_file_path)

    def c_compile_run():
        global opened_file_path
        system("gcc -O3 " + opened_file_path + "-o a.exe & a & pause")
        top.title("编译运行c程序" + opened_file_path)

    def java_compile_run():
        global opened_file_path
        system("javac " + opened_file_path + "& java " + opened_file_path +
                ".class" + "& pause")
        top.title("编译运行java程序" + opened_file_path)

    def c_i():
        global opened_file_path
        system("gcc -O3 -E " + opened_file_path + " -o a.i")
        top.title(opened_file_path)

    def c_s_intel():
        global opened_file_path
        system("gcc -O3 -S -masm=intel " + opened_file_path + " -o a.s")
        top.title("把" + opened_file_path + "编译成intel的汇编语言")

    def rm():
        global open_file_path
        from os import remove
        remove(open_file_path)
        top.title("已永久删除" + open_file_path)

    def remv():
        from win32com.shell import shell, shellcon
        global open_file_path
        top.title("删除" + open_file_path)
        shell.SHFileOperation((0, shellcon.FO_DELETE, open_file_path, None,
                                shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO
                                | shellcon.FOF_NOCONFIRMATION, None, None))

    def import_colors():
        with popen("python colors.pyw") as _:
            print(_.read())
        top.title("颜色表")

    def pydoc1():
        top.title("python第三方包文档")
        system("python -m pydoc " + message.get() + "& pause")

    def pydoc3():
        top.title("python第三方包文档")
        if message.get() == '':
            system("python -m pydoc -p 80 & pause")
        else:
            system("python -m pydoc -p " + message.get() + "& pause")

    def tit():
        top.title(message.get())

    def pdb_debug():
        top.title("调试")
        system("python -m pdb " + message.get() + " & pause")

    def pythoni():
        top.title("运行python程序后运行交互式python")
        system("python -i " + message.get())

    def speed():
        system("python -m cProfile " + message.get() + "& pause")

    def dirdir():
        root = Tk()
        root.title("显示目录下的文件")
        root.geometry("1000x700")
        _ = run(["dir", "/a", "/q"], shell=True, stdout=PIPE)
        Label(root, text=_.stdout.decode("gb2312")).pack(side=TOP)
        mainloop()

    def yapfyapf():
        global opened_file_path
        system("yapf -i " + opened_file_path)

    def requirement_install():
        system("pip install -r requirement.txt & pause")

    def python_version():
        from platform import python_version
        messagebox.showinfo("python版本", python_version())
        top.title("python版本")

    def alert_file_byte():
        global opened_file_path
        from os.path import getsize
        top.title("显示字节数")
        messagebox.showinfo("约" + str(getsize(opened_file_path)) + "字节",
                            "约" + str(getsize(opened_file_path)) + "字节")

    def pip_help():
        system("pip help & pause")

    def coverage_run():
        system("coverage run " + message.get() + "& pause")

    def coverage_report():
        system("coverage report -m " + message.get() + "& pause")

    def coverage_html():
        system("coverage html -d report" + "& pause")

    def on_closing():
        if contents.get('1.0', END).strip():
            save()
            top.destroy()
        else:
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
            self.daemon = True
            self.start()

        def Run(self):
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

    def mypy_type():
        system("mypy " + message.get())

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
        else:
            process_key(event)

    bifs = dir(__builtins__)
    kws = kwlist
    top = Tk()
    top.title("邢栋的集成开发环境")
    top.geometry('1520x700')
    hook_dropfiles(top, func=dragged_load)
    menubar = Menu(top)
    contents = ScrolledText(font=40)
    contents.pack(side=BOTTOM, expand=True, fill=BOTH)
    top.protocol("WM_DELETE_WINDOW", on_closing)
    contents.bind('<KeyRelease>', on_key_release)
    contents.bind('<Control-o>', lambda event: load())
    contents.bind('<Control-S>', lambda event: resave())  #Ctrl+Shift+s
    contents.bind('<Control-N>', lambda event: run(["python", abspath(__file__)], shell=True))  #Ctrl+Shift+n
    contents.tag_config('bif', foreground='tomato')
    contents.tag_config('kw', foreground='deepskyblue')
    contents.tag_config('comment', foreground='purple')
    contents.tag_config('string', foreground='green')
    Label(text=abspath(__file__), fg='red').pack(side=LEFT)
    message = Entry(font=40)
    message.pack(side=LEFT, expand=True, fill=X)
    menu1 = Menu(menubar, tearoff=False)
    menu1.add_command(label='打开文件', command=load)
    menu1.add_command(label='保存文件', command=save)
    menu1.add_command(label='另存为文件', command=resave)
    menu1.add_command(label='隐藏文件',
                        command=run(["attrib", "+H",
                                    message.get()]))
    menu1.add_command(label='恢复隐藏的文件',
                        command=run(["attrib", "-H",
                                    message.get()]))
    menu1.add_command(label='只读文件',
                        command=run(["attrib", "+R",
                                    message.get()]))
    menu1.add_command(label='解除只读文件',
                        command=run(["attrib", "-R",
                                    message.get()]))
    menu1.add_command(label='显示字节数', command=alert_file_byte)
    menu1.add_command(label='创建文件夹', command=md)
    menu1.add_command(label='删除文件夹', command=rd)
    menu1.add_command(label='清理python缓存', command=python_cache)
    menu1.add_command(label='删除文件', command=remv)
    menu1.add_command(label='永久删除文件', command=rm)
    menubar.add_cascade(label="文件管理", menu=menu1)
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
    menu2.add_command(label='pip帮助', command=lambda: MyThread(pip_help))
    menu2.add_command(label='检查依赖', command=lambda: MyThread(pip_check))
    menu2.add_command(label='搜索', command=lambda: MyThread(pip_search))
    menu2.add_command(label='查看信息', command=lambda: MyThread(pip_show))
    menu2.add_command(label='用requirement.txt中的包安装',
                        command=lambda: MyThread(requirement_install))
    menu2.add_command(label='下载安装包', command=lambda: MyThread(pip_download))
    menu2.add_command(label='卸载', command=lambda: MyThread(pip_uninstall))
    menu2.add_command(label='重新安装',
                        command=lambda: MyThread(pip_install_uninstall))
    menu2.add_command(label='升级', command=lambda: MyThread(pip_upgrade))
    menu2.add_command(label='安装', command=lambda: MyThread(pip_install))
    menubar.add_cascade(label="python第三方包管理器", menu=menu2)
    top.config(menu=menubar)
    menu3 = Menu(menubar, tearoff=False)
    menu3.add_command(label='运行python程序', command=lambda: MyThread(python_run))
    menu3.add_command(label='用ipython运行python程序',
                        command=lambda: MyThread(ipython_run))
    menu3.add_command(label='运行python程序后运行交互式python',
                        command=lambda: MyThread(pythoni))
    menu3.add_command(label='把python程序编译成命令行的exe',
                        command=lambda: MyThread(pyinstaller_exe_c))
    menu3.add_command(label='把python程序编译成可视化的exe',
                        command=lambda: MyThread(pyinstaller_exe_w))
    menu3.add_command(label='编译c程序', command=lambda: MyThread(c_compile))
    menu3.add_command(label='预处理c程序', command=lambda: MyThread(c_i))
    menu3.add_command(label='编译c程序成汇编语言', command=lambda: MyThread(c_s_intel))
    menu3.add_command(label='编译运行c程序', command=lambda: MyThread(c_compile_run))
    menu3.add_command(label='运行go程序', command=lambda: MyThread(go_run))
    menu3.add_command(label='把go程序编译成exe文件',
                        command=lambda: MyThread(go_build))
    menu3.add_command(label='编译java程序', command=lambda: MyThread(java_compile))
    menu3.add_command(label='运行java程序', command=lambda: MyThread(java_run))
    menu3.add_command(label='编译运行java程序',
                        command=lambda: MyThread(java_compile_run))
    menubar.add_cascade(label="编译与运行", menu=menu3)
    top.config(menu=menubar)
    menu4 = Menu(menubar, tearoff=False)
    menu4.add_command(label='dos', command=lambda: MyThread(system("cmd")))
    menu4.add_command(label='python',
                        command=lambda: MyThread(system("python")))
    menu4.add_command(label='ipython',
                        command=lambda: MyThread(system("ipython")))
    menu4.add_command(label='ptpython',
                        command=lambda: MyThread(system("ptpython")))
    menu4.add_command(label='bpython',
                        command=lambda: MyThread(system("bpython")))
    menu4.add_command(label='powershell',
                        command=lambda: MyThread(system("powershell")))
    menubar.add_cascade(label="命令行", menu=menu4)
    top.config(menu=menubar)
    menu5 = Menu(menubar, tearoff=False)
    menu5.add_command(label='命令行', command=lambda: MyThread(pydoc1))
    menu5.add_command(label='所有第三方包的网页版', command=lambda: MyThread(pydoc3))
    menubar.add_cascade(label="第三方包文档", menu=menu5)
    top.config(menu=menubar)
    menu6 = Menu(menubar, tearoff=False)
    menu6.add_command(label='显示运行速度', command=speed)
    menu6.add_command(label='用pdb调试', command=lambda: MyThread(pdb_debug))
    menubar.add_cascade(label='python调试', menu=menu6)
    top.config(menu=menubar)
    menu7 = Menu(menubar, tearoff=False)
    menu7.add_command(label='修改为1号风格（默认）', command=normal_theme)
    menu7.add_command(label='修改为2号风格', command=other_theme)
    menu7.add_command(label='修改为3号风格', command=third_theme)
    menu7.add_command(label='修改为4号风格', command=fourth_theme)
    menubar.add_cascade(label='语法高亮风格', menu=menu7)
    top.config(menu=menubar)
    menu8 = Menu(menubar, tearoff=False)
    menu8.add_command(label='生成测试文件并运行',
                        command=lambda: MyThread(coverage_run))
    menu8.add_command(label='显示结果', command=lambda: MyThread(coverage_report))
    menu8.add_command(label='生成html文件夹',
                        command=lambda: MyThread(coverage_html))
    menubar.add_cascade(label='python测试覆盖率', menu=menu8)
    top.config(menu=menubar)
    menu9 = Menu(menubar, tearoff=False)
    menu9.add_command(label='init', command=lambda: MyThread(git_init))
    menu9.add_command(label='add', command=lambda: MyThread(git_add))
    menu9.add_command(label='clone', command=lambda: MyThread(git_clone))
    menu9.add_command(label='commit', command=lambda: MyThread(git_commit))
    menu9.add_command(label='diff', command=lambda: MyThread(git_diff))
    menubar.add_cascade(label='git', menu=menu9)
    top.config(menu=menubar)
    Button(
        text='再启动一个窗口',
        command=lambda: MyThread(run(["python", abspath(__file__)], shell=True)
                                    )).pack(side=RIGHT)
    Button(text='浏览器', command=lambda: MyThread(liulanqi)).pack(side=RIGHT)
    Button(text='计算器',
            command=lambda: MyThread(run("calc", shell=True))).pack(side=RIGHT)
    Button(text='死亡之ping',
            command=lambda: MyThread(hack_ping)).pack(side=RIGHT)
    Button(text="yapf格式化", command=lambda: MyThread(yapfyapf)).pack(side=RIGHT)
    Button(text='创建虚拟环境', command=lambda: MyThread(vtenv)).pack(side=RIGHT)
    Button(text='颜色表',
            command=lambda: MyThread(import_colors)).pack(side=RIGHT)
    Button(text='修改标题', command=tit)
    Button(text='类型检查', command=lambda: MyThread(mypy_type)).pack(side=RIGHT)
    Button(text='百度', command=lambda: MyThread(baidu)).pack(side=RIGHT)
    Button(text='python官网',
            command=lambda: MyThread(pythonorg)).pack(side=RIGHT)
    Button(text='python版本',
            command=lambda: MyThread(python_version)).pack(side=RIGHT)
    Button(text="显示目录文件", command=dirdir).pack(side=RIGHT)
    mainloop()
except Exception as e:
    print(e)
