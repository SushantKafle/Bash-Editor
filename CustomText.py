import Tkinter as tk
import re
from Highlighter import Highlighter
from Helper import Helper

class CustomText(tk.Text):

    keywordSelection = False
    currentDir = ""
    home=""
    lib=""
    env=""
    
    def __init__(self,*args, **kwargs):
        self.line = kwargs.pop("line")
        tk.Text.__init__(self, *args, **kwargs)
        self.highlighter = Highlighter()
        self.helper = Helper()
        self.tag_configure("current_line", background="#e9e9e9")
        self._highlight_current_line()

    def _highlight_current_line(self, interval=100):
    	
        self.tag_remove("current_line", 1.0, "end")
        if not self.tag_ranges("sel"):
            self.tag_delete("selKeyword")
            self.tag_add("current_line", "insert linestart", "insert lineend+1c")
            line,column = self.index("insert").split(".")
            self.line.configure(text="Line: "+line+", Column: "+str(int(column)+1))
        else:
	    self.findSimilarWords()
	    	
        self.after(interval, self._highlight_current_line)
        

    def findSimilarWords(self):
        seltext = self.get("sel.first", "sel.last")
        if not " " in seltext:
            self.markKeyword(seltext)
    

    def markKeyword(self,keyword):
        self.tag_delete("selKeyword")
        self.tag_configure("selKeyword", background="#99e9e9")

        start = self.index("1.0")
        end = self.index("end")
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            word = self.get("matchStart","matchStart wordend")
            
            if word==keyword:
                self.keywordSelection = True
                self.tag_add("selKeyword", "matchStart","matchStart wordend")
            
            self.mark_set("matchStart", '%s+%dc' % ("matchStart", len(word)))
            
            if self.index("matchStart") == self.index("end"):
                break


    def highlight_line(self, pattern, tag, start="1.0", end="end", regexp=False):
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            
            self.mark_set("matchEnd", "%s lineend" % index)
            self.tag_add(tag, "matchStart","matchEnd")

    def highlight_q(self):
    
    	self.tag_delete("red")
        self.tag_configure("red", foreground = "#f05050")

        self.tag_delete("green")
        self.tag_configure("green", foreground = "#50f050")

        data = self.get("1.0","end")
        
        indices = self.highlighter.highlight_quotes(data)
        for index in indices:
        	if len(index) > 1:
	            self.tag_add("red", index[0], index[1])
            
	

    def basicHighlights(self,lineComment):
        if len(lineComment)==0:
            return 

        self.tag_delete("quote")
        self.tag_configure("quote", foreground = "#33ae33")

        data = self.get("1.0","end")

        #self.helper.smart_update(data,self.currentDir)

        #self.helper.update(self.currentDir)
        
        [qindices,cindices] = self.highlighter.basicHighlights(data,lineComment)

        for index in qindices:
        	if len(index) > 1:
	            self.tag_add("quote", index[0], index[1])

        self.tag_delete("comment")
        self.tag_configure("comment", foreground = "brown")

        #comments = self.highlighter.line_comment(data,lineComment)
	
	for index in cindices:
            if len(index) > 1:
	            self.tag_add("comment", index[0], index[1])

    def highlight_func(self,func,funcStart):
        if len(func)==0:
            return
        
        self.tag_delete("func")
        self.tag_configure("func", foreground = "blue")

        data = self.get("1.0","end")
        funcs = self.highlighter.highlight_func(data,func,funcStart)
	
	for index in funcs:
            if len(index) > 1:
	            self.tag_add("func", index[0], index[1])
        


    def setfocus(self,exp):

        #data = self.get("1.0","end")
        index = self.search(exp, "1.0", "end", count=tk.IntVar(), regexp=True)
        self.see(index)
        self.focus()
        
    
    def highlight_keyword(self, patterns):
        start = self.index("1.0")
        end = self.index("end")
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        self.tag_delete("keyword")
        self.tag_configure("keyword", foreground = "#FFA50A")
        
        count = tk.IntVar()
        while True:
            word = self.get("matchStart","matchStart wordend")
            
            if word in patterns:
                self.tag_add("keyword", "matchStart","matchStart wordend")
            
            self.mark_set("matchStart", '%s+%dc' % ("matchStart", len(word)))
            
            if self.index("matchStart") == self.index("end"):
                break
