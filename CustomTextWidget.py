from Tkinter import *
import ttk
import tkFileDialog
from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *

from CustomText import CustomText

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
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
        text.bind("<Control-a>", self.selectall)
        text.bind("<Control-s>", self.save)
        text.bind("<Key>", self.key)

    def save(self,event):
        if len(self.filename) == 0:
            self.filename = asksaveasfilename()
        if  self.filename:
            print self.filename
            alltext = self.gettext()                      
            open(self.filename, 'w').write(alltext)
    
    def selectall(self, event):
        self.text.tag_add(SEL, '1.0', END)     
        self.text.mark_set(INSERT, '1.0')         
        self.text.see(INSERT)                    
        self.text.focus()
        return "break"
    
    def key(self,event):
        data = self.text.get("1.0",END)
        lineNum = (len(data.split("\n"))-1)
        self.setKeywords();
    
    def setKeywords(self):
        self.text.tag_delete("blue")
        self.text.tag_configure("blue", foreground = "blue")
        keywords = []
        commentSigns = []
        if ".ksh" in self.filename:
            keywords = ["alias","bg","builtin","break","case","cd","command","continue","disown","echo","exec","exit","export","eval","FALSE","fg","for","function","getconf","getopts","hist","if","jobs","kill","let","newgrp","print","printf","pwd","read","readonly","return","select","set","shift","sleep","test","time","trap","TRUE","typeset","ulimit","umask","unalias","unset","until","wait","whence","while","do","done","esac","fi","then"]
            commentSigns = ["#"]
        elif ".py" in self.filename:
            keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']
            commentSigns = ["#"]

        self.text.highlight_keyword(keywords, "blue")
        self.text.tag_delete("green")
        self.text.tag_configure("green", foreground = "green")
        for commentSign in commentSigns:
            self.text.highlight_line(commentSign, "green")
            
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)
        self.setKeywords();
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

        #self.text.tag_delete("current_line")
        #self.text.tag_configure("current_line", background="#e9e9e9")
        #self.text.tag_add("current_line", "insert linestart", "insert lineend")
        
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')
