import re
class Highlighter():

    quotes = []
    pre_meta_data = {}

    def getMetaData(self, data):
        meta = {}
        for i,line in enumerate(data.split("\n")):
            meta[i]=len(line)

        return meta
            
    def copy_matches(self, matches):
        result = []
        for match in matches:
            result.append([match.start(0), match.end(0)])
        return result

    def highlight_line_comment(self, data, symbol):
        re_comment = r""+symbol+"(.*)"
        comments = self.copy_matches(re.finditer(re_comment,data))
        result = list(tuple(comments))
        
        if len(self.quotes) == 0:
            return self.getIndices(comments, self.pre_meta_data)
        
        for q in self.quotes:
            for c in comments:
                if q[0] < c[0] and q[1] > c[0]:
                    result.remove(c)
                
        return self.getIndices(result, self.pre_meta_data)
        
            
    def highlight_quotes(self, data):
        self.pre_meta_data = self.getMetaData(data)
        re_quote = r"([\"'])((?:(?!\1)[^\\]|(?:\\\\)*\\[^\\])*)\1"
        self.quotes = self.copy_matches(re.finditer(re_quote, data,re.DOTALL))
        return self.getIndices(self.quotes, self.pre_meta_data)


    def getIndices(self, matches, meta):
        indices = []
        c_indices = 0

        if len(matches) == 0:
            return []

        if len(meta) == 0:
            return []

        for match in matches:
            maxLength = 0
            char_count = 0
            p_start = False
            for i in range(len(meta)):
                maxLength += meta[i]+1
                
                if match[0] <= maxLength and not p_start:
                    indices.append([str(i+1)+"."+str(match[0]-char_count)])
                    p_start = True
                
                if match [1] <= (maxLength+1) and p_start:
                    indices[c_indices].append(str(i+1)+"."+str(match[1]-char_count))
                    c_indices += 1
                    p_start = False
                    break
            
                char_count += meta[i]+1
            
        return indices
