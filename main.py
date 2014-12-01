from Tkinter import * 
from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.var = StringVar()
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        self.settext(text, file)
        
        
        
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        self.line = Label(self, text="1")
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)
        self.line.grid(row=0,column=0, sticky=N)
        text.grid(row=0,column=1)
        sbar.grid(row=0,column=2, sticky=E+W+N+S)
        self.text = text
        text.bind("<Key>", self.key)

    def key(self,event):
        data = self.text.get("1.0",END)#
        lineNum = (len(data.split("\n"))-1)
        self.line.config(text=self.getLineArray(lineNum))

    def getLineArray(self, lineNum):
        num = ""
        for i in range(lineNum):
            num += str(i+1)+"\n"
        return num
        
        
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

        data = self.text.get("1.0",END)#
        lineNum = (len(data.split("\n"))-1)
        self.line.config(text=self.getLineArray(lineNum))
        
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')
        

class SimpleEditor(ScrolledText):                        
    def __init__(self, parent=None, file=None):
        
        frm = Frame(parent)
        frm.pack(fill=X)

        parent.title("Simple menu")
        
        menubar = Menu(parent)
        parent.config(menu=menubar)
        
        fileMenu = Menu(menubar,tearoff=0)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_command(label="Exit", command=self.onQuit)

        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Copy", command= self.onCopy)
        editMenu.add_command(label="Cut", command= self.onCut)
        editMenu.add_command(label="Paste", command= self.onPaste)
        editMenu.add_command(label="Find", command= self.onFind)

        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Edit", menu=editMenu)
        
        ScrolledText.__init__(self, parent, file=file)
        
        self.text.config(font=('courier', 9, 'normal'))
        
    def onQuit(self):
        ans = askokcancel('Confirm exit', "Sure you want to Quit?")
        if ans: self.quit()
        
    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()                      
            open(filename, 'w').write(alltext)

    def onCopy(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)
        
    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)           
        self.clipboard_clear()              
        self.clipboard_append(text)
        
    def onPaste(self):                                    
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass
        
    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            try:
                where = self.text.search(target,SEL_FIRST, SEL_LAST)
            except TclError:
                where = self.text.search(target, 1.0, END)
            if where:                                    
                pastit = where + ('+%dc' % len(target))     
                self.text.tag_add(SEL, where, pastit)     
                self.text.mark_set(INSERT, pastit)         
                self.text.see(INSERT)                    
                self.text.focus()                        

#if there are no cmdline arguments, open a new file.
root = Tk()

if len(sys.argv) > 1:
	app = SimpleEditor(root,file=sys.argv[1])                
else: 
        app = SimpleEditor(root)
root.mainloop()
