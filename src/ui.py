#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
#Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
from tkinter.messagebox import *
#from tkinter import filedialog  #.askopenfilename()
#from tkinter import simpledialog  #.askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Form1')
        self.master.geometry('579x331')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TFrame1.TLabelframe', font=('宋体',9))
        self.style.configure('TFrame1.TLabelframe.Label', font=('宋体',9))
        self.Frame1 = LabelFrame(self.top, text='配置文件路径', style='TFrame1.TLabelframe')
        self.Frame1.place(relx=0.014, rely=0.628, relwidth=0.969, relheight=0.196)

        self.Command1Var = StringVar(value='点击打开或者拖拽文件')
        self.style.configure('TCommand1.TButton', font=('宋体',9))
        self.Command1 = Button(self.top, text='点击打开或者拖拽文件', textvariable=self.Command1Var, command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.setText = lambda x: self.Command1Var.set(x)
        self.Command1.text = lambda : self.Command1Var.get()
        self.Command1.place(relx=0.014, rely=0.024, relwidth=0.983, relheight=0.583)

        self.Command2Var = StringVar(value='配置编辑器')
        self.style.configure('TCommand2.TButton', font=('宋体',9))
        self.Command2 = Button(self.top, text='配置编辑器', textvariable=self.Command2Var, command=self.Command2_Cmd, style='TCommand2.TButton')
        self.Command2.setText = lambda x: self.Command2Var.set(x)
        self.Command2.text = lambda : self.Command2Var.get()
        self.Command2.place(relx=0.76, rely=0.846, relwidth=0.223, relheight=0.124)

        self.Command3Var = StringVar(value='运     行')
        self.style.configure('TCommand3.TButton', font=('宋体',9))
        self.Command3 = Button(self.top, text='运     行', textvariable=self.Command3Var, command=self.Command3_Cmd, style='TCommand3.TButton')
        self.Command3.setText = lambda x: self.Command3Var.set(x)
        self.Command3.text = lambda : self.Command3Var.get()
        self.Command3.place(relx=0.014, rely=0.846, relwidth=0.734, relheight=0.124)

        self.Text1Var = StringVar(value='Text1')
        self.Text1 = Entry(self.Frame1, textvariable=self.Text1Var, font=('宋体',9))
        self.Text1.setText = lambda x: self.Text1Var.set(x)
        self.Text1.text = lambda : self.Text1Var.get()
        self.Text1.place(relx=0.014, rely=0.246, relwidth=0.971, relheight=0.631)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        super().__init__(master)

    def Command1_Cmd(self, event=None):
        #TODO, Please finish the function here!
        pass

    def Command2_Cmd(self, event=None):
        #TODO, Please finish the function here!
        pass

    def Command3_Cmd(self, event=None):
        #TODO, Please finish the function here!
        pass

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()



