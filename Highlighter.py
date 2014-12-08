import re
class Highlighter():

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
            
    def highlight_quotes(self, data):
        pre_meta_data = self.getMetaData(data)
        re_quote = r"([\"'])((?:(?!\1)[^\\]|(?:\\\\)*\\[^\\])*)\1"
        return self.getIndices(self.copy_matches(re.finditer(re_quote, data)), pre_meta_data)


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
