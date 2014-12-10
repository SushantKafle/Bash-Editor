import re

class Helper():

    #dict of all the documents included in the script
    linkedDocs = []
    
    #dict of all the variables exported
    variables = {}
    
    #dict of all the linked functions (in and out of the documents)
    functions = {}

    #dict of all the default values
    defaults = {}

    def init(self, values):
        # values = { "key": [list]}
        self.defaults = values

    def update(self,data):

        self.variables = {}
        self.linkedDocs = []

        #in the document
        for lineNum,line in enumerate(data.split("\n")):
            try:
                #may be line executed something
                if line.replace(" ","")[0] == ".":
                    r_ex = r".(.*)"
                    path = re.findall(r_ex,line)
                    for p in path:
                        self.linkedDocs.append([p.replace(" ",""),lineNum])
                
                #may be a function is defined
                else:
                    r_func = r"function(.*){"
                    func = re.findall(r_func, line)
                    for f in func:
                        self.functions[f.replace(" ","")]="."
            except:
                continue

        print self.containsVar(self.linkedDocs[0][0])
        print self.functions

    def resolve(self, value, data):
        var = self.containsVar(value[0], True)
        pos = value[1]
        #if var:
            
        

    def containsVar(self, val,param=False):
        r_v = r"\${([^}]*)}"
        print val
        searchObj = re.findall(r_v,val)
        if searchObj:
            if(param): return searchObj[-1][:-1]
            else: return True
        return False

    #def resolveExternalLinks(self):
        
                
                

    
