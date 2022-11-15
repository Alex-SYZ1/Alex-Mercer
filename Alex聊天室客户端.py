#coding=utf-8
from tkinter import *
from datetime import *
from socket import *
import threading
import tkinter
import tkinter.messagebox
try:
    from PIL import Image,ImageTk
    import emoji#请pip install --upgrade emoji==1.6.3
    from ej import *
except:
    print("请先在cmd安装如下所需的包：","1.pillow   pip install pillow","2.emoji's v1.6.3   pip install --upgrade emoji==1.6.3",sep="\n")
    import sys
    sys.exit(0)
from tkinter.scrolledtext import ScrolledText

ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'  # 时间格式声明
s = socket()  # 套接字
global demo
# 登录窗口
def Login_gui_run():
    root = Tk()
    root.title("聊天系统·登录")  # 窗口标题
    frm = Frame(root)

    root.geometry('300x150+200+200')  # 窗口大小

    nickname = StringVar()  # 昵称变量
    server_IP=StringVar() #ip变量
    def login_in():  # 登录函数（检查用户名是否为空，以及长度）
        name = nickname.get()  # 长度是考虑用户列表那边能否完整显示
        if not name:
            tkinter.messagebox.showwarning('Warning', message='用户名为空！')
        elif len(name) > 10:
            tkinter.messagebox.showwarning('Warning', message='用户名过长！最多为十个字符！')
        else:
            root.destroy()
            s.connect((server_IP.get(), 3000))  # 建立连接
            s.send(nickname.get().encode('utf-8'))  # 传递用户昵称
            Chat_gui_run()  # 打开聊天窗口

    # 登录按钮、输入提示标签、输入框
    Button(root, text="登录", command=login_in, width=8, height=1).place(x=100, y=100, width=100, height=35)
    Label(root, text='请输入昵称', font=('Fangsong', 12)).place(x=10, y=20, height=50, width=80)
    Entry(root, textvariable=nickname, font=('Fangsong', 11)).place(x=130, y=30, height=30, width=140)
    Label(root,text="请输入服务器IP", font=('Fangsong', 12)).place(x=8, y=55, height=50)
    Entry(root,textvariable=server_IP, font=('Fangsong', 11)).place(x=130, y=64, height=30, width=140)
    root.mainloop()


# 聊天窗口
def Chat_gui_run():
    window = Tk()
    window.maxsize(650, 400)  # 设置相同的最大最小尺寸，将窗口大小固定
    window.minsize(650, 400)
    
    stateVar=StringVar()
    stateVar.set("对所有人说:")
    user_choosed=StringVar()
    user_choosed.set("点此对用户进行操作")
    var1 = StringVar()
    user_list = []
    user_list = s.recv(2048).decode('utf-8').split(',')  # 从服务器端获取用户列表
    user_dict={key:2 for key in user_list}#私聊为1,屏蔽为0,默认为2
    
    nickname = user_list[len(user_list) - 1]  # 获取正式昵称，经过了服务器端的查重修改
    window.title("聊天系统--" + nickname)  # 设置客户端窗口昵称
    var1.set(user_list)  # 用户列表文本设置
    #var1.set([1,2,3,5])
    
    Label(text="------用户列表------").place(x=510, y=0, width=140, height=18)
    listbox1 = Listbox(window, listvariable=var1)  # 用户列表，使用Listbox组件
    listbox1.place(x=510, y=18, width=140, height=182)
    listbox = ScrolledText(window,state="disabled",font=('华文楷体', '14',"bold"))  # 聊天信息窗口，使用ScrolledText组件制作
    listbox.place(x=5, y=0, width=500, height=300)
        
    def a(event):print(listbox1.curselection())#perfect
    def popupmenu(event):
        menuUser.post(event.x_root,event.y_root)
    def block_sb(num):#屏蔽操作
        num=int(str(num)[1:-2])
        name=user_list[num]
        if name== nickname:
            tkinter.messagebox.showinfo("提示","您无法拉黑自己")
            return
        if name in user_dict:
            user_dict[name]=0
            user_list[num]=f"{user_list[num]}(已屏蔽)"
            var1.set(user_list)
        else:
            user_list[num]=user_list[num][:-5]
            var1.set(user_list)
            user_dict[user_list[num]]=2

    def help_menu():#查看帮助
        global show_ornot
        top = Toplevel()
        top.attributes("-topmost",True)
        top.title("聊天室功能介绍")
        top.geometry("600x180")
        top.maxsize(600,180)
        #sb = Scrollbar(top)               # 创建Scrollbar组件
        #sb.pack(side='right', fill='y')
        msg = Text(top,height=11,width=1,cursor="heart",exportselection=False)
        msg.config(exportselection=False)
        msg.place(x=10,y=0,width=590,height=600)
        #sb.config(command=msg.yview)
        msg.tag_config('tag_head', font=('华文楷体', '11',"bold"), foreground='#db7093'\
                       ,background="#4d4dff")
        msg.tag_config('tag_1', font=('华文楷体', '11',"bold"), foreground='#ef7782'\
                       ,background="#4da6ff")
        msg.tag_config('tag_2', font=('华文楷体', '11',"bold"),foreground='#3d3b4f'\
                       ,background="#a64dff")
        msg.tag_config('tag_big',\
                       font=('华文楷体', '17',"bold"),background="#A61840",foreground='#FCDFB7')
        msg.tag_config("tag_key",font=('华文楷体', '11'),foreground='#ff4500'\
                       ,background="#00ffc4")
        msg.tag_config("tag_head1",font=('华文楷体', '11'),foreground='#FCDFB7'\
                       ,background="#A61840")
        emojis=emoji.emojize('欢迎来到Alex聊天室！ :thumbsup:\n',use_aliases=True)
        msg.insert("end",emojis,"tag_big")
        rule=["本聊天室具有以下特色：","发送emoji表情、发送常用语、对用户开启或关闭屏蔽/私聊操作，具体介绍如下：",\
              "①发送emoji。","点击emoji按钮，在输入框、聊天框中均可显示为emoji小表情;","②发送常用语。","点击常用语按钮选择常用语，自动插入到输入框的末尾;",\
              "③屏蔽/私聊操作。","在用户列表中使用鼠标左键双击任意用户，即可弹出开『开启/关闭屏蔽操作、开启/关闭私聊操作』的菜单。"]
        tags=["tag_head","tag_head1","tag_key","tag_head","tag_key","tag_1","tag_key","tag_2","tag_key","tag_head"]
        for i in range(len(rule)):
            msg.insert("end",rule[i]+"\n",tags[i])
        
    help_menu()
    def direct_TOsb(num):#私聊操作
        
        num=int(str(num)[1:-2])
        name=user_list[num]#获取对方昵称
        if name== nickname:
            tkinter.messagebox.showinfo("提示","您无法与自己私聊")
            return
        if name not in user_dict:tkinter.messagebox.showinfo("提示","您无法与已屏蔽的人进行私聊操作")
        elif user_dict[name]==1:
            user_dict[name]=2
            stateVar.set("对所有人说:")
        else:
            user_dict[name]=1
            stateVar.set(f"对{name}悄悄说")
    def initialize(button):
        if user_list[num]==nickname:tkinter.messagebox.showinfo("提示","您无法对自己进行屏蔽或私聊操作")
        
    menuUser = Menu(window, tearoff=False)
    
    menuUser.add_command(label="开启/关闭屏蔽操作", command=lambda:block_sb(listbox1.curselection()))
    menuUser.add_command(label="开启/关闭私聊操作", command=lambda:direct_TOsb(listbox1.curselection()))
    listbox1.bind('<Double-Button-1>',popupmenu)

    #window.config(menu=menuUser)
    
    user_choose=Frame()
    user_choose.place(x=510,y=200,height=100,width=140)
    demo=ImageTk.PhotoImage(Image.open("demo.jpg"))
    Label(user_choose,text="请点此按钮查看帮助！",compound="bottom",font=('微软雅黑',10),image=demo,).pack()
    Button(user_choose,text="HELP",command=help_menu,font=('Fixdsys',15)).place(x=85,y=20)
    
    
    # 接收服务器发来的消息并显示到聊天信息窗口上，与此同时监控用户列表更新
    def read_server(s):
        while True:
            
            content = emoji.emojize(s.recv(2048).decode('utf-8'))  # 接收服务器端发来的消息
            print(content)
            Blocked=False
            for i in user_dict:
                if user_dict[i]!=0:continue
                print(i)
                if content.startswith(f"{i}悄悄对你说:") or content.startswith(f"{i}说:"):
                    Blocked=True
                    break
            if Blocked==False:
                if content!="":listbox.config(state="normal")
                curtime = datetime.now().strftime(ISOTIMEFORMAT)  # 获取系统时间
                listbox.insert(tkinter.END, curtime)  # 聊天信息窗口显示（打印）
                listbox.insert(tkinter.END, '\n' + content + '\n')
                listbox.see(tkinter.END)  # ScrolledText组件方法，自动定位到结尾，否则只有消息在涨，窗口拖动条不动
                listbox.update()  # 更新聊天信息窗口，显示新的信息
                listbox.config(state="disabled")
            # 判断新的信息是否为系统消息
            if content[0:5] == '系统消息：':
                person=content[5:content.find(' ')]
                if content[content.find(' ') + 1: content.find(' ') + 3] == '进入':
                    user_list.append(person)
                    var1.set(user_list)
                    user_dict[person]=2
                if content[content.find(' ') + 1: content.find(' ') + 3] == '离开':
                    user_list.remove(person)
                    var1.set(user_list)
                    del user_dict[person]
    threading.Thread(target=read_server, args=(s,)).start()

    sb = Scrollbar()               # 创建Scrollbar组件
    sb.place(x=5, y=305,height=95)
    talkstate=Label(window,textvariable=stateVar,font=('华文楷体', '10',"bold"))
    talkstate.place(x=5,y=305,height=10)
    entryInput = Text(window, width=140,yscrollcommand=sb.set,cursor="heart",font=('华文楷体', '17',"bold"))
    entryInput.place(x=5, y=315, width=600, height=85)
    sb.config(command=entryInput.yview)

    # 发送按钮触发的函数，即发送信息
    def sendtext():
        receiver=stateVar.get()
        print(receiver)
        line = emoji.demojize(entryInput.get("1.0","end"))
        line=line[:-1] if line[-2:]=="\n\n" else line
        if receiver !="对所有人说:":
            line=receiver+":"+line
        print(line)
        s.send(line.encode('utf-8'))
        entryInput.delete("1.0","end")  # 发送完毕清空聊天输入口
    def sendemoji():
        choose=Toplevel()
        choose.title("#")#请选择您想要插入输入框的emoji
        choose.attributes("-topmost",True)
        
        choose.geometry("500x300+750+60")
        ej_sb = Scrollbar(choose)               # 创建Scrollbar组件
        ej_sb.pack(side='right', fill='y')
        ejs = Text(choose, width=188,bg="black",height=188,yscrollcommand=sb.set,cursor="heart")
        ejs.pack()
        ej_sb.config(command=ejs.yview)
        
        emojis=list(ej_dict.values())
        draw(ejs,entryInput,Button)
        ejs.config(state="disabled")

    # 添加emoji按钮
    sendButton = Button(window, text='emoji', bg='white', command=sendemoji,relief="ridge")
    sendButton.place(x=610, y=305)

    # 常用语按钮
    normalButton = Menubutton(window, text='常用语', bg='white',relief="ridge")
    normalButton.place(x=608, y=337)
    
    editmenu=Menu(normalButton,tearoff=False)
    ####syz
    editmenu.add_command(label="你没事儿吧？",command=lambda :entryInput.insert("end","你没事儿吧？") )
    editmenu.add_command(label="不好意思，不想和你聊天",command=lambda :entryInput.insert("end","不好意思，不想和你聊天") )
    normalButton.config(menu=editmenu)
    # 发送按钮
    sendButton = Button(window, text='发 送', bg='white', command=sendtext,relief="ridge")
    sendButton.place(x=610, y=370)
    def quick_send(event):sendtext()
    window.bind("<Return>",quick_send)
    window.mainloop()


Login_gui_run()
#s.connect(('10.1.69.119', 3000))  # 建立连接
#s.send("Alex".encode('utf-8'))  # 传递用户昵称     测试用
Chat_gui_run()  # 打开聊天窗口"""
