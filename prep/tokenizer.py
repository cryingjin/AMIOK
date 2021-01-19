from konlpy.tag import Mecab

def mecab_tokenizer(text):
    # print("\ntokenizing...")
    tagger = Mecab()
    npo = tagger.morphs(text) #pos없는 버젼
    ypo = tagger.pos(text) #pos있는 버젼

    return npo, ypo

