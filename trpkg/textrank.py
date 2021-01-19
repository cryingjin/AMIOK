import networkx
import re
import prep.tokenizer as tk
import prep.preprocess as prep

# Sentence Extraction
class RawSentence:
    def __init__(self, textIter):
        if type(textIter) == str: self.textIter = textIter.split('\n')
        else: self.textIter = textIter
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')
 
    def __iter__(self):
        for line in self.textIter:
            # print("line : ", line)
            # str로 들어온 문장을 특수문자와 일반문자를 구분하여 list형태로 저장 
            ch = self.rgxSplitter.split(line)
            # print("ch : ", ch)
            # print("ch[::2]: ",ch[::2], "ch[1::2]:", ch[1::2])
            # 문장과 점을 이어붙여 완전한 문장의 형태로 만들고 반환함. 
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                # print("map s : ", s)
                if not s: continue
                yield s

class TextRank:
    def __init__(self, **kargs):
        self.graph = None
        self.window = kargs.get('window', 7)
        self.coef = kargs.get('coef', 1.0)
        self.threshold = kargs.get('threshold', 0.005)
        self.dictCount = {}
        self.dictBiCount = {}
        self.dictNear = {}
        self.nTotal = 0
 
 
    def loadSents(self, sentenceIter, tokenizer = None):
        import math
        # Similarity
        def similarity(a, b):
            n = len(a.intersection(b))
            return n / float(len(a) + len(b) - n) / (math.log(len(a)+1) * math.log(len(b)+1))
 
        if not tokenizer: rgxSplitter = re.compile('[\\s.,:;-?!()"\']+')
        sentSet = []
        for sent in filter(None, sentenceIter):
            if type(sent) == str:
                if tokenizer: s = set(filter(None, tokenizer(sent)))
                else: 
                    s = set(filter(None, rgxSplitter.split(sent)))
            else: s = set(sent)
            #해당 문장을 토크나이저로 자른 형태들, 2보다 작다면 이는 여기서 NNG, NN, VV, VA을 포함하는 요소가 아예 없거나 하나밖에 없다는 뜻
            if len(s) < 2: 
                continue
            self.dictCount[len(self.dictCount)] = sent
            sentSet.append(s)
            #sentSet : {('아버지', 'NNG'), ('식당', 'NNG')} 등의 형태로 문장의 토큰들을 저장한 곳.

        #모든 문장의 조합에 대해서 similarity 계산 후 dicBiCount에 저장.
        for i in range(len(self.dictCount)):
            for j in range(i+1, len(self.dictCount)):
                s = similarity(sentSet[i], sentSet[j])
                if s < self.threshold: continue
                self.dictBiCount[i, j] = s
 

    def build(self):
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.dictCount.keys())
        for (a, b), n in self.dictBiCount.items():
            self.graph.add_edge(a, b, weight=n*self.coef + (1-self.coef))
 
    def rank(self):
        return networkx.pagerank(self.graph, weight='weight')
  
    def summarize(self, ratio = 0.333):
        r = self.rank()
        ks = sorted(r, key=r.get, reverse=True)
        score = int(len(r)*ratio)

        if score < 5 : 
            score = len(r) 
        elif score >= 5:
            score = 5
        else:
            pass
        
        ks = ks[:score]
        return ' '.join(map(lambda k:self.dictCount[k], sorted(ks)))


def sentence_extraction(text):
    tr = TextRank()
    tagger = tk.Mecab()
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV') ])
    tr.loadSents(RawSentence(text), lambda sent: filter(lambda x:x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'), tagger.pos(sent)))
    tr.build()
    ranks = tr.rank()
    result = tr.summarize(0.5)
    # When the textrank result is nan
    if result == "":
        result = text
    
    #result에 스펠검사 한번 더 
    result = prep.spell_check(result)
    return result

'''
https://bab2min.tistory.com/570 해당 링크를 참고해 코드를 구현하였습니다. 
'''
