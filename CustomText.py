import Tkinter as tk

from Highlighter import Highlighter

class CustomText(tk.Text):
    
    def __init__(self,*args, **kwargs):
        self.line = kwargs.pop("line")
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_configure("current_line", background="#e9e9e9")
        self._highlight_current_line()

    def _highlight_current_line(self, interval=100):
        self.tag_remove("current_line", 1.0, "end")
        self.tag_add("current_line", "insert linestart", "insert lineend+1c")
        line,column = self.index("insert").split(".")
        self.line.configure(text="Line: "+line+", Column: "+str(int(column)+1))
        self.after(interval, self._highlight_current_line)

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

    def highlight_q(self, tag):
        highlighter = Highlighter()
        
        indices = highlighter.highlight_quotes(self.get("1.0","end"))
        for index in indices:
            self.tag_add(tag, index[0], index[1])
    
    def highlight_quotes(self, tag, start="1.0", end="end", regexp=True):
        start = self.index(start)
        end = self.index(end)
        
        self.mark_set("dmatchStart", start)
        self.mark_set("dmatchEnd", start)
        self.mark_set("searchLimit", end)

        doubleQuotes = []
        
        count = tk.IntVar()
        while True:
            dindex1 = self.search(r'\"', "dmatchEnd","searchLimit", count=count, regexp=regexp)

            if dindex1 == "": break
            
            
            dtemp = int(dindex1.split(".")[1])+1
            dindx1 = ".".join([dindex1.split(".")[0], str(dtemp)])
            
            dindex2 = self.search(r'\"',dindx1,"searchLimit", count=count, regexp=regexp)

            if dindex2 == "": dindex2 = "end"
            
            
            dtemp = int(dindex2.split(".")[1])+1
            dindx2 = ".".join([dindex2.split(".")[0], str(dtemp)])
            
            self.tag_add(tag, dindex1, dindx2)

            #break
            
            #self.mark_set("matchStart",str(float(index1)+(0.1)))
            
            self.mark_set("dmatchEnd", dindx2)
            
    

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index,count.get()))
            self.tag_add(tag, "matchStart","matchEnd")

    def highlight_keyword(self, patterns, tag, start="1.0", end="end", regexp=False):
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            word = self.get("matchStart","matchStart wordend")
            
            if word in patterns:
                self.tag_add(tag, "matchStart","matchStart wordend")
            
            self.mark_set("matchStart", '%s+%dc' % ("matchStart", len(word)))
            
            if self.index("matchStart") == self.index("end"):
                break
