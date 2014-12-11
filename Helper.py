import re
import os.path

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

    def update(self,data,curDir):
        self.curDir = curDir
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
            
        searchableData = data
        inrLength = 0
        loop = len(self.linkedDocs)
        for i in range(loop):
                pos = self.linkedDocs[i][1]
                self.linkedDocs[i] = [self.resolve(self.linkedDocs[i],searchableData,inrLength),pos]
                print self.linkedDocs
                searchableData,binr = self.appendData(searchableData, self.linkedDocs[i],inrLength)
                print binr
                inrLength += binr 

        self.getAllFunctions();

    def getAllFunctions(self):
        for docs in self.linkedDocs:
            path,pos = docs
            if os.path.isfile(path):
                docData = open(path,'r').read()
                for line in docData.split("\n"):
                    r_func = r"function(.*){"
                    func = re.findall(r_func,line)
                    for f in func:
                        self.functions[f.replace(" ","")]=path
 

    def appendData(self,data,doc,inr):
        print doc[1],inr
        print data
        pos2insert = doc[1]+inr
        if os.path.isfile(doc[0]):
            newData = open(doc[0],'r').read()
            lines = data.split("\n")
            length = len(lines)
            print lines[pos2insert]
            lines[pos2insert] = newData
            return ['\n'.join(lines),length]

        return [data,0]

    def resolve(self, variable, data, inr):
        var = self.containsVar(variable[0], True)
        pos = variable[1]
        value = ""
        if var:
            if var=="HOME":
                return variable[0].replace("${HOME}",self.curDir)
            
            #search the document bottom to top above it for the variable
            for i,line in enumerate(data.split("\n")):
                if i > (pos+inr-1):
                    break

                #search for value in line
                r_value = r""+var+"=(.*)"
                buff = re.search(r_value,line)
                if buff:
                    value = self.resolve([buff.group(1),i],data,inr)

            #replace variable with value
            if len(value) > 0:
                return variable[0].replace("${"+var+"}",value)
            
            
        return variable[0]    

    def containsVar(self, val,param=False):
        r_v = r"\${([^}]*)}"
        searchObj = re.findall(r_v,val)
        if searchObj:
            if(param): return searchObj[-1]
            else: return True
        return False

    def getFunctionParam(self,name):
        if name in self.functions:
            return self.functions[name]
        return ""
        
                
                

    
