# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2024-05-30 09:36:14.265723
# @Last Modified by: CPS
# @Last Modified time: 2024-05-30 09:36:14.265723
# @file_path "W:\CPS\MyProject\projsect_persional\python-tk-ui-learn\src"
# @Filename "test2.py"
# @Description: 功能描述
#

import tkinter, os

from tkinter.messagebox import showwarning

from src.ui.main import Application
from src.config import Config
from src.events import UI_Events


def check(config: Config):
    if float(tkinter.TkVersion) < 8.6:
        showwarning("版本过低提示", "注意，当前tk版本过低，可能存在未知问题")

    # 校验config对象
    pass


class UI(UI_Events, Application):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, config: Config):
        check(config)

        main_tk = tkinter.Tk()
        super().__init__(main_tk)

        self.master.title(config.title)

        screenWidth = main_tk.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = main_tk.winfo_screenheight()  # 获取显示区域的高度
        left = int((screenWidth - config.width) / 2)  # 定位x
        top = int((screenHeight - config.height) / 2 * 0.8)  # 定位y

        self.master.geometry(f"{config.width}x{config.height}+{left}+{top}")
        if config.dragged_file_enable:
            self.init_dragged_file()

        self.createWidgets()
        self.process_start()

    def process_start(self):
        self.mainloop()

    def init_dragged_file(self):
        import windnd

        def dragged_files(files, encodeing="gbk"):
            if len(files) > 1:
                showwarning("文件太多", "仅支持单个文件识别")
            self.Text1Var.set(files[0].decode(encodeing))

        windnd.hook_dropfiles(self.master, func=dragged_files)


def start_with_ui():
    config = Config

    UI(config)


if __name__ == "__main__":
    start_with_ui()
