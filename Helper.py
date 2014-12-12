import re
from os import listdir
from os.path import isfile, join, isdir

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

    def update(self,param={}):
        files = []
        self.functions={}
        if 'lib' in param:
            LIB_DIR = param['lib']
            if isdir(LIB_DIR):
                files = [LIB_DIR+"/"+f for f in listdir(LIB_DIR) if isfile(join(LIB_DIR,f))]
            
        if 'env' in param:
            ENV_FILE = param['env']
            if isfile(ENV_FILE):
                files.append(ENV_FILE)
        
        for f in files:
            data = open(f,'r').read()
            for line in data.split("\n"):
                r_func = r"function(.*)"
                func = re.findall(r_func,line)
                for fu in func:
                    self.functions[fu.replace(" ","").replace("{","")]=f

    def smart_update(self,data,curDir):
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

        for i,doc in enumerate(self.linkedDocs):
            pos = self.linkedDocs[i][1]
            self.linkedDocs[i] = [self.resolve(self.linkedDocs[i],searchableData,inrLength),pos]
            searchableData,binr = self.appendData(searchableData, self.linkedDocs[i],inrLength)
            inrLength += binr

        self.getAllFunctions();
        #print "---\n",self.linkedDocs
        #print self.functions,"\n-----\n"

    def getAllFunctions(self):
        for docs in self.linkedDocs:
            path,pos = docs
            if isfile(path):
                docData = open(path,'r').read()
                #print docData
                for line in docData.split("\n"):
                    r_func = r"function(.*)"
                    func = re.findall(r_func,line)
                    for f in func:
                        self.functions[f.replace(" ","").replace("{","")]=path
 

    def appendData(self,data,doc,inr):
        pos2insert = doc[1]+inr
        if isfile(doc[0]):
            newData = open(doc[0],'r').read()
            for lineNum,line in enumerate(newData.split("\n")):
                try:
                    #may be line executed something
                    if line.replace(" ","")[0] == ".":
                        r_ex = r".(.*)"
                        path = re.findall(r_ex,line)
                        for p in path:
                            self.linkedDocs.append([p.replace(" ",""),lineNum])
                except:
                    continue
            lines = data.split("\n")
            length = len(newData.split('\n'))
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
        
                
                

    
