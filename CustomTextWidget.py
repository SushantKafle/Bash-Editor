from Tkinter import *
import ttk
import tkFileDialog
from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *

from time import time

from CustomText import CustomText

class ScrolledText(Frame):
    
    keyTimeStamp = 0

    def __init__(self, parent=None, text='', file=None):
        self.parent = parent
        Frame.__init__(self, parent)
        self.filename = ""
        self.var = StringVar()
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)

    def makewidgets(self):
        sbar = Scrollbar(self)
        line = Label(self, text="Line: 1, Column: 1")
        text = CustomText(self, line=line, relief=SUNKEN, background="#fefefe")
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        text.grid(row=0,column=0,sticky=E+W+N+S)
        sbar.grid(row=0,column=1, sticky=E+W+N+S)
        line.grid(row=1,column=0, sticky="E")
        self.text = text
        text.bind("<Key>", self.key)
        text.bind("<Control-Button-1>", self.helperSupport)

    def key(self,event):
        if (time() - self.keyTimeStamp) > 0.5:
            #self.text.highlight_q()
            self.setKeywords()
        self.keyTimeStamp= time()
    
    def setKeywords(self):
        keywords = []
        lineComment = ""
        function = ""
        functionStart = ""
        if ".ksh" in self.filename:
            keywords = ["alias","bg","builtin","break","case","cd","command","continue","disown","echo","exec","exit","export","eval","FALSE","fg","for","function","getconf","getopts","hist","if","jobs","kill","let","newgrp","print","printf","pwd","read","readonly","return","select","set","shift","sleep","test","time","trap","TRUE","typeset","ulimit","umask","unalias","unset","until","wait","whence","while","do","done","esac","fi","then"]
            lineComment = "#"
            function = "function"
            functionStart = "{"
        elif ".py" in self.filename:
            keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']
            lineComment = "#"
            function = "def"
            functionStart = ":"
            
        elif ".sh" in self.filename:
            keywords = ["alias","bg","builtin","break","case","cd","command","continue","disown","echo","exec","exit","export","eval","FALSE","fg","for","function","getconf","getopts","hist","if","jobs","kill","let","newgrp","print","printf","pwd","read","readonly","return","select","set","shift","sleep","test","time","trap","TRUE","typeset","ulimit","umask","unalias","unset","until","wait","whence","while","do","done","esac","fi","then"]
            lineComment = "#"
            function = "function"
            functionStart = "{"
            
        self.text.highlight_func(function, functionStart)
        self.text.highlight_keyword(keywords)
        self.text.basicHighlights(lineComment)
            
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)
        #self.text.highlight_q()
        self.setKeywords();
        self.text.mark_set(INSERT, '1.0')
        self.text.edit_modified(False)
        self.text.focus()
        
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')

    def helperSupport(self,event):
        name = self.text.get('current wordstart','current wordend')
        filename = self.text.helper.getFunctionParam(name)
        if filename != "":
            if filename == ".":
                self.text.setfocus(r"function "+name)
            else:
                self.text.filename = filename
                self.parent.title(filename+" Bash Editor")
                self.settext(self.text, filename)
                self.text.setfocus(r"function "+name)
            
