import tkinter  # 导入tkinter模块
items = []  # 初始化选项列表root = tkinter.Tk()  # 创建窗口

root = tkinter.Tk()
root.title('lambda+for代码程序')  # 设置标题root.geometry('500x300')  # 设置窗口大小为500x300
root.resizable(width=False, height=False)  # 禁止修改窗口大小

for item in ('A', 'B', 'C', 'D'):  # 循环定义
    tkinter.Button(root, text=item, command=lambda: items.append(item)).pack()


def show() -> None:  # 顺便说一句， -> None表示返回None. 也可以是bool, tuple, tkinter.Misc等等
    print(items)


tkinter.Button(root, text='输出已选选项', command=show).pack()

root.mainloop()  # 窗口持久化
