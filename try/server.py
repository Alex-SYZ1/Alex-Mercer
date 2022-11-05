import copy
import time as tm
from socket import *
from sqlite3 import connect
import threading
from datetime import *
# -*- coding: utf-8 -*-"""function discreption:Created on Mon Oct 18 11:16:34 2021To: One is never too old to learn!@author: puyuanwei"""
# 炸金花
from random import sample
from collections import Counter

IP = '192.168.0.102'                 
PORT = 30000
HOST= gethostbyname(gethostname())
IP=HOST
print("服务器IP地址为："+HOST)
# 时间格式声明，用于后面的记录系统时间
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

def socket_target(s, nickname,number):                         
        global match
        while True:
            
            content =s.recv(2048).decode('utf-8')                     # 获取用户发送的消息
            curtime = datetime.now().strftime(ISOTIMEFORMAT)    # 系统时间打印
                print(curtime)
                print(nickname+'说：'+content)
                with open('serverlog.txt', 'a+') as serverlog:      # log记录
                    serverlog.write(str(curtime) + '  ' + nickname + '说：' + content + '\n')
                for client in socket_list:                          # 其他套接字通知
                   client.send((nickname + '说:'+ content).encode('utf-8'))

def going(number,b,c):#运行服务器并连接客户端
 
    # 聊天记录存储至当前目录下的serverlog.txt文件中
    try:
        with open('serverlog.txt', 'a+') as serverlog:                    
            curtime = datetime.now().strftime(ISOTIMEFORMAT)
            serverlog.write('\n\n-----------服务器打开时间：'+str(curtime)+'，开始记录聊天-----------\n')
    except:
        print('ERROR!')
    # 读取套接字连接
    s = socket()
    s.bind((IP, PORT))
    s.listen()
    while True:                                                     # 不断接受新的套接字进来，实现“多人”
        conn, addr = s.accept()                                     # 获取套接字与此套接字的地址
        socket_list.append(conn)                                    # 套接字列表更新
        print(number,b,c)
        conn.send((f"玩家数量{number}+游戏底注{b}+游戏本金{c}" ).encode('utf-8'))
        nickname = conn.recv(2048).decode('utf-8')                  # 接受昵称
        again=0
        if nickname in user_list:                                   # 昵称查重，相同则在后面加上数字
            i = 1
            again=1
            while True:
                if nickname+str(i) in user_list:
                    i = i + 1
                else:
                    nickname = nickname + str(i)
                    break
     
        user_list.append(nickname)                                  # 用户列表更新，加入新用户（新的套接字）
        curtime = datetime.now().strftime(ISOTIMEFORMAT)
        print(curtime)
        print(nickname + ' 进入了游戏!')
        if again==1:
            socket_list[-1].send(f"由于姓名重复，您的昵称被自动替换为{nickname}"
                                         .encode('utf-8'))
            tm.sleep(1)
        with open('serverlog.txt', 'a+') as serverlog:              # log记录
            serverlog.write(str(curtime) + '  ' + nickname + ' 进入了游戏!\n')
            
