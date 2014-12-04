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
        
        re_single_quote = r"'([^'\\]*(?:\\.[^'\\]*)*)'"
        re_double_quote = r'"([^"\\]*(?:\\.[^"\\]*)*)"'

        double_matches = re.finditer(re_double_quote, data, re.DOTALL | re.VERBOSE)
        single_matches = re.finditer(re_single_quote, data, re.DOTALL | re.VERBOSE)
        
        actual_matches = []

        double_matches = list(double_matches)
        single_matches = list(single_matches)
        
        if len(single_matches)==0:
            actual_matches = self.copy_matches(double_matches)
        elif len(double_matches)==0:
            actual_matches = self.copy_matches(single_matches)
        else:
            actual_matches = self.copy_matches(double_matches) + self.copy_matches(single_matches)

            for d_match in double_matches:
                for s_match in single_matches:
                    d_start = d_match.start(0)
                    d_end = d_match.end(0)

                    s_start = s_match.start(0)
                    s_end = s_match.end(0)
                    
                    if(d_start < s_start and d_end > s_start):
                        actual_matches.remove([s_start, s_end])
                    elif(d_start > s_start and d_start < s_end):
                        actual_matches.remove([d_start, d_end])

                    '''else:
                        actual_matches.append([d_start, d_end])
                        actual_matches.append([s_start, s_end])'''
                        
        return self.getIndices(actual_matches, pre_meta_data)


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
