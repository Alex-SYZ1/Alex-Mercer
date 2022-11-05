#coding=utf-8
from tkinter import *
from datetime import *
from socket import *
import threading
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import emoji#请pip install --upgrade emoji==1.6.3

ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'  # 时间格式声明
s = socket()  # 套接字


# 登录窗口
def Login_gui_run():
    root = Tk()
    root.title("聊天系统·登录")  # 窗口标题
    frm = Frame(root)

    root.geometry('300x150')  # 窗口大小

    nickname = StringVar()  # 昵称变量

    def login_in():  # 登录函数（检查用户名是否为空，以及长度）
        name = nickname.get()  # 长度是考虑用户列表那边能否完整显示
        if not name:
            tkinter.messagebox.showwarning('Warning', message='用户名为空！')
        elif len(name) > 10:
            tkinter.messagebox.showwarning('Warning', message='用户名过长！最多为十个字符！')
        else:
            root.destroy()
            s.connect(('127.0.0.1', 30000))  # 建立连接
            s.send(nickname.get().encode('utf-8'))  # 传递用户昵称
            Chat_gui_run()  # 打开聊天窗口

    # 登录按钮、输入提示标签、输入框
    Button(root, text="登录", command=login_in, width=8, height=1).place(x=100, y=90, width=100, height=35)
    Label(root, text='请输入昵称', font=('Fangsong', 12)).place(x=10, y=20, height=50, width=80)
    Entry(root, textvariable=nickname, font=('Fangsong', 11)).place(x=100, y=30, height=30, width=180)

    root.mainloop()


# 聊天窗口
def Chat_gui_run():
    window = Tk()
    window.maxsize(650, 400)  # 设置相同的最大最小尺寸，将窗口大小固定
    window.minsize(650, 400)

    var1 = StringVar()
    user_list = []
    user_list = s.recv(2048).decode('utf-8').split(',')  # 从服务器端获取用户列表
    user_list.insert(0, '------用户列表------')

    nickname = user_list[len(user_list) - 1]  # 获取正式昵称，经过了服务器端的查重修改
    window.title("聊天系统--" + nickname)  # 设置窗口标题，体现用户专属窗口（不是）
    var1.set(user_list)  # 用户列表文本设置
    # var1.set([1,2,3,5])
    listbox1 = Listbox(window, listvariable=var1)  # 用户列表，使用Listbox组件
    listbox1.place(x=510, y=0, width=140, height=300)
    
    listbox = ScrolledText(window,state="disabled")  # 聊天信息窗口，使用ScrolledText组件制作
    listbox.place(x=5, y=0, width=500, height=300)

    # 接收服务器发来的消息并显示到聊天信息窗口上，与此同时监控用户列表更新
    def read_server(s):
        while True:
            listbox.config(state="normal")
            content = emoji.emojize(s.recv(2048).decode('utf-8'))  # 接收服务器端发来的消息
            print(content)
            curtime = datetime.now().strftime(ISOTIMEFORMAT)  # 获取系统时间
            listbox.insert(tkinter.END, curtime)  # 聊天信息窗口显示（打印）
            listbox.insert(tkinter.END, '\n' + content + '\n\n')
            listbox.see(tkinter.END)  # ScrolledText组件方法，自动定位到结尾，否则只有消息在涨，窗口拖动条不动
            listbox.update()  # 更新聊天信息窗口，显示新的信息
            listbox.config(state="disabled")
            # 判断新的信息是否为系统消息
            if content[0:5] == '系统消息：':
                if content[content.find(' ') + 1: content.find(' ') + 3] == '进入':
                    user_list.append(content[5:content.find(' ')])
                    var1.set(user_list)
                if content[content.find(' ') + 1: content.find(' ') + 3] == '离开':
                    user_list.remove(content[5:content.find(' ')])
                    var1.set(user_list)

    threading.Thread(target=read_server, args=(s,)).start()

    sb = Scrollbar()               # 创建Scrollbar组件
    sb.place(x=5, y=305,height=95)
    entryInput = Text(window, width=140,yscrollcommand=sb.set,cursor="heart")
    entryInput.insert("end",emoji.emojize('初始规则：:thumbsup: ',use_aliases=True))
    entryInput.place(x=5, y=305, width=600, height=95)
    sb.config(command=entryInput.yview)

    # 发送按钮触发的函数，即发送信息
    def sendtext():
        
        line = emoji.demojize(entryInput.get("1.0","end"))
        print(line)
        s.send(line.encode('utf-8'))
        entryInput.delete("1.0","end")  # 发送完毕清空聊天输入口
    def sendemoji():
        choose=Toplevel()
        choose.title("#")#请选择您想要插入输入框的emoji
        choose.attributes("-topmost",True)
        choose.geometry("188x188+600+200")
        ej_sb = Scrollbar(choose)               # 创建Scrollbar组件
        ej_sb.pack(side='right', fill='y')
        ejs = Text(choose, width=188,bg="black",height="188",yscrollcommand=sb.set,cursor="heart")
        ejs.pack()
     
        ej_sb.config(command=ejs.yview)
        sss=emoji.emojize(':thumbsup:',use_aliases=True)

        creator=Button(ejs,command=lambda:insert_ej(sss),text=sss)
        ejs.window_create('end', window=creator)
        
        ejs.config(state="disabled")
        def insert_ej(a):
            entryInput.insert("end",a)
        
        pass
    # 添加emoji按钮
    sendButton = Button(window, text='emoji', bg='white', command=sendemoji)
    sendButton.place(x=610, y=305)

    # 常用语按钮
    sendButton = Button(window, text='常用语', bg='white', command=sendtext)
    sendButton.place(x=608, y=337)
    
    # 发送按钮
    sendButton = Button(window, text='发 送', bg='white', command=sendtext)
    sendButton.place(x=610, y=370)

    window.mainloop()


#Login_gui_run()
s.connect(('127.0.0.1', 30000))  # 建立连接
s.send("syz".encode('utf-8'))  # 传递用户昵称
Chat_gui_run()  # 打开聊天窗口
