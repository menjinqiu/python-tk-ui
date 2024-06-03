# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2024-05-30 16:35:13.961047
# @Last Modified by: CPS
# @Last Modified time: 2024-05-30 16:35:13.961047
# @file_path "W:\CPS\MyProject\projsect_persional\python-tk-ui-learn\src"
# @Filename "events.py"
# @Description: 这是一个类似事件中心的组件，对应ui.py的Application类中所有回调方法
#
import os, sys

sys.path.append("..")

from src.utils.tk_utils import selectPath


class UI_Var:
    Text1Var = "文件路径选择输入框，使用self.Text1Var.get()"


class UI_Events:
    def Command1_Cmd(self, event=None):
        # 点击按钮打开文件的调用
        sel_path = selectPath("file")
        if sel_path:
            if os.path.exists(sel_path):
                self.Text1Var.set(sel_path)
            # showinfo("已选配置文件：", sel_path)

    def Command2_Cmd(self, event=None):
        # 拖拽文件到识别区域的调用
        print("Command2_Cmd")
        # showinfo("Command2_Cmd", self.Text1Var.get())
