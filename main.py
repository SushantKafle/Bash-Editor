from Tkinter import *
import ttk
import tkFileDialog
from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *

import os
import glob

from CustomTextWidget import ScrolledText

class SimpleEditor(ScrolledText):                        
    def __init__(self, parent=None, file=None):
        
        frm = Frame(parent)
        frm.pack(fill=X)

        parent.title("Bash Editor")
        
        menubar = Menu(parent)
        parent.config(menu=menubar)
        
        fileMenu = Menu(menubar,tearoff=0)
        fileMenu.add_command(label="Open Project", command=self.askDirectory)
        fileMenu.add_command(label="Open File", command=self.askopenfilename)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_command(label="Save As", command=self.onSaveAs)
        fileMenu.add_command(label="Exit", command=self.onQuit)

        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Copy", command= self.onCopy)
        editMenu.add_command(label="Cut", command= self.onCut)
        editMenu.add_command(label="Paste", command= self.onPaste)
        editMenu.add_command(label="Find", command= self.onFind)
        editMenu.add_command(label="SelectAll", command= self.onSelectAll)

        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Edit", menu=editMenu)
        
        vsb = Scrollbar(orient="vertical")
        hsb = Scrollbar(orient="horizontal")
        
        self.tree = ttk.Treeview(columns=("fullpath", "type", "size"),
        displaycolumns="size")
        
        self.tree.heading("#0", text="Directory Structure", anchor='w')
        self.tree.heading("size", text="File Size", anchor='w')
        self.tree.column("size", stretch=0, width=100)

        self.populate_roots(self.tree)
        self.tree.bind('<<TreeviewOpen>>', self.update_tree)
        self.tree.bind('<Double-Button-1>', self.change_dir)
        
        self.tree.pack(side=LEFT, fill=Y)
        ScrolledText.__init__(self, parent, file=file)
        
        self.text.config(font=('Lucida Console', 10, 'normal'))

    def populate_tree(self,tree, node):
        if tree.set(node, "type") != 'directory':
            return
        path = tree.set(node, "fullpath")
        tree.delete(*tree.get_children(node))

        parent = tree.parent(node)
        special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

        for p in special_dirs + os.listdir(path):
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p): ptype = "directory"
            elif os.path.isfile(p): ptype = "file"

            fname = os.path.split(p)[1]
            id = tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    tree.insert(id, 0, text="dummy")
                    tree.item(id, text=fname)
            elif ptype == 'file':
                size = os.stat(p).st_size
                tree.set(id, "size", "%d bytes" % size)


    def populate_roots(self,tree, path=''):
        if len(path) == 0:
            dir = os.path.abspath('.').replace('\\', '/')
        else:
            dir = path
        
        node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
        self.populate_tree(tree, node)

    def update_tree(self,event):
        tree = event.widget
        self.populate_tree(tree, tree.focus())

    def change_dir(self,event):
        tree = event.widget
        node = tree.focus()
        if tree.parent(node):
            path = os.path.abspath(tree.set(node, "fullpath"))
            if os.path.isdir(path):
                
                os.chdir(path)
                tree.delete(tree.get_children(''))
                self.populate_roots(tree)
            elif os.path.isfile(path):
                self.filename = path
                self.settext(self.text, path)

    def autoscroll(self,sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def askopenfilename(self):
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        if filename:
            fileRoot ='/'.join(filename.split("/")[:-1])
            self.filename = filename
            self.settext(self.text, filename)
            if os.path.isdir(fileRoot):
                self.tree.delete(self.tree.get_children(''))
                self.populate_roots(self.tree,fileRoot)
            

    def askDirectory(self):
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        path = tkFileDialog.askdirectory(**self.dir_opt)
        self.tree.delete(self.tree.get_children(''))
        self.populate_roots(self.tree,path)
        return 
        
        
    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END)     
        self.text.mark_set(INSERT, '1.0')         
        self.text.see(INSERT)                    
        self.text.focus()
        return "break"
        
    def onQuit(self):
        ans = askokcancel('Confirm exit', "Sure you want to Quit?")
        if ans: self.quit()
        
    def onSave(self):
        if len(self.filename) == 0:
            self.filename = asksaveasfilename()
        if  self.filename:
            print self.filename
            alltext = self.gettext()                      
            open(self.filename, 'w').write(alltext)

    def onSaveAs(self):
        self.filename = asksaveasfilename()
        if  self.filename:
            print self.filename
            alltext = self.gettext()                      
            open(self.filename, 'w').write(alltext)
            

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
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()
