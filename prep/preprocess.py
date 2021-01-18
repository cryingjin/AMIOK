import kss
import re
from hanspell import spell_checker

def clean_text(text):
    text = re.sub(r'[@%\\*=()/~&\+á?\xc3\xa1\-\|\:\;\!\-\,\_\~\$\'\"\“]', '', text) #remove punctuation 
    text = re.sub(r'\.\.+', '.', text) #점이 두 개 이상 반복되는 부분 제거
    text = re.sub(r'\u200B', '', text) #폭 없는 공백 제거
    text = text.lower() #lower case 
    text = re.sub(r'\s+', ' ', text) #remove extra space 
    text = re.sub(r'<[^>]+>','',text) #remove Html tags
    text = re.sub(r'\s+', ' ', text) #remove spaces
    text = re.sub(r"^\s+", '', text) #remove space from start 
    text = re.sub(r'\s+$', '', text) #remove space from the end
    text = re.sub(r'\.', '', text) #점 제거
    return text

def sentence_split(text):
    sen = []
    for sent in kss.split_sentences(text):
        sen.append(sent)
    result = '. '.join(sen)
    return result

def clean_question(text):
    text = re.sub(r'^\.', '',text) #맨 앞에 문자가 아닌 것이 등장한 경우
    text = re.sub(r'\s+\.$', '', text) #맨 뒤에 문자가 아닌 것이 등장한 경우 
    text = re.sub(r'\s+\.\s+', '', text) #무의미한 .이 들어있는 경우 - (3)번
    text = re.sub(r"^\s+", '', text) #remove space from start 
    text = re.sub(r'\s+$', '', text) #remove space from the end
    text = re.sub('[|ㄱ-ㅎ|ㅏ-ㅣ]+', '', text) # 3) ㅠㅠ, ㅋㅋ, ㅎㅎ 등 자음만 혹은 모음만 있는 경우 제거
    text = re.sub('…', '', text) # 4) … 제거
    text = re.sub('❌', '', text) # 5) 이모티콘 제거

    # (2)번 마침표 뒤에 스페이스 없는 경우 스페이스 추가.
    while re.search('[가-힣]\.\S', text):
        mats = re.search('\w\.\S', text)
        start = mats.span()[0]
        end = mats.span()[1]
        text = text[:start+2]+' '+text[end-1:]

    # 1) 문장 끝에 ..이 오는 경우 .으로 수정
    while re.search('[가-힣]\.\.\s', text):
        text = re.sub(r'\.\.', '\.', text)

    # 2) 문장 중간 혹은 시작할 때 .. 이 오는 경우 제거
    text = re.sub(r'\.\.', '', text) 
    return text

def spell_check(text):
    if len(text) >= 500:
        pass
    else:
        text = spell_checker.check(text).as_dict()["checked"]
    return text

def preprocess(sen):
    sen = clean_text(sen)
    sen = sentence_split(sen)
    sen = clean_question(sen)
    sen = spell_check(sen)
    return sen

