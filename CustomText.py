import Tkinter as tk

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

    def highlight_quotes(self, tag, start="1.0", end="end", regexp=True):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index1 = self.search(r'\"', "matchEnd","searchLimit", count=count, regexp=regexp)

            if index1 == "": break
            
            
            temp = int(index1.split(".")[1])#+1
            indx1 = ".".join([index1.split(".")[0], str(temp)])
            
            index2 = self.search(r'\"',indx1,"searchLimit", count=count, regexp=regexp)

            if index2 == "": index2 = "end"
            
            
            temp = int(index2.split(".")[1])#+1
            indx2 = ".".join([index2.split(".")[0], str(temp)])
            
            self.tag_add(tag, index1, indx2)

            break

            #break
            
            #self.mark_set("matchStart",str(float(index1)+(0.1)))
            
            self.mark_set("matchEnd", indx2)
            
    

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
