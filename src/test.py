import tkinter as tk
from tkinter import Toplevel, Button


def create_subwindow():
    # 获取主窗口的几何信息
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()

    # 设置子窗口的初始位置，紧接在主窗口右边，并有一个间距（例如20像素）
    sub_window_x = root_x + root_width + 5
    sub_window_y = root.winfo_y()  # 或者你可以设置一个固定的y值，使子窗口与主窗口顶部对齐

    # 创建一个新的Toplevel窗口，并设置其初始位置
    sub_window = Toplevel(root)
    sub_window.geometry(f"+{sub_window_x}+{sub_window_y}")  # 设置位置和大小（例如 300x200）
    sub_window.title("子窗口")

    # 在这里，你可以添加子窗口的其他组件
    label = tk.Label(sub_window, text="这是一个子窗口")
    label.pack(pady=20)


# 创建主窗口
root = tk.Tk()
root.title("主窗口")
root.geometry("300x200")  # 设置主窗口的大小，以便测试位置

# 创建一个按钮，点击时调用create_subwindow函数
button = Button(root, text="打开子窗口", command=create_subwindow)
button.pack(pady=20)

# 进入主事件循环
root.mainloop()
