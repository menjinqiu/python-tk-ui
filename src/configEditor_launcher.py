# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2024-06-13 17:19:03.808006
# @Last Modified by: CPS
# @Last Modified time: 2024-06-13 17:19:03.808006
# @file_path "W:\CPS\MyProject\projsect_persional\python-tk-ui-learn\src"
# @Filename "configEditor_launcher.py"
# @Description: 子窗口的启动器，注册事件，重新配置窗体属性等
#
import os, sys
import tkinter

sys.path.append("..")

from src.ui.configEditor import Application
from src.events.configEditorEvents import Events


class SubWindowConfig:
    title: str
    width: int
    height: int
    lef: int
    top: int
    master: tkinter.Tk


class UI(Events, Application):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, config: SubWindowConfig):
        sub_tk = tkinter.Tk()
        super().__init__(sub_tk)

        self.master.title(config.title)
        self.master.geometry(f"{config.width}x{config.height}+{config.left}+{config.top}")


if __name__ == "__main__":
    config = SubWindowConfig()
    UI(config)
