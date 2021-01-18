import prep.preprocess as prep
import re
from random import randint
import kss

def sentence_split(text):
    sen = []
    for sent in kss.split_sentences(text):
      sen.append(sent)
    return '. '.join(sen)


def remove_dup(text):
    sen_split = text.split('.')
    lst_sens = []

    for sen1 in range(len(sen_split)):
        lst_sens.append(sen_split[sen1].strip())

    lst_num = []

    for sen2 in range(len(lst_sens)):
        if lst_sens[sen2] in lst_sens[sen2+1:]:
            lst_num.append(sen2)

    lst_total_num = list(range(len(lst_sens)))
    lst_final_num = list(set(lst_total_num).difference(lst_num))

    lst_final = []
    for sen3 in lst_final_num:
        plus_dot = lst_sens[sen3] + '.'
        lst_final.append(plus_dot)

    result = ' '.join(lst_final)
    return result


def clean(text, remove_lst=[]):
    # 문장 제거 (전처리한 데이터로 인퍼런스한 결과를 보면서 제거할 문장 여기에 추가)
    for r in remove_lst:
        text = re.sub(r, '', text)
    
    # 기호 및 띄어쓰기 제거
    text = re.sub('[^ A-Za-z0-9가-힣.]+', '', text) # 한글, 영어, 숫자, 띄어쓰기 제외 제거
    text = re.sub(' +', '', text) # 띄어쓰기 두칸 이상 한칸으로 바꾸기
    text = re.sub('\.\.+', '.', text) # 온전 두개를 한개로 바꾸기
    
    # 반말 -> 높임말로 수정
    text = re.sub('이다', '입니다', text)
    text = re.sub('않다', '않습니다', text)
    text = re.sub('꾼다\.', '꿉니다.', text)
    text = re.sub('뿐이다\.', '뿐입니다.', text)
    text = re.sub('아니다', '아닙니다', text)
    text = re.sub('쓴다', '씁니다', text)
    text = re.sub('있다', '있습니다', text)
    text = re.sub('pad', '', text)

    
    return text


def add_sentence(text):
    before_sentences =[
        '안녕하세요. 두빅스입니다. 질문자분의 내용 잘 보았습니다. ',
        '반갑습니다. 두빅스입니다. 그런 사연이 있으셨군요. ',
        '안녕하십니까. 두빅스입니다. 많이 힘드셨겠습니다. '
    ]
    
    after_sentences =[
        ' 아무쪼록 도움이 되셨길 바라며, 쾌유하시길 바라겠습니다.',
        ' 제 답변이 도움이 되었길 바랍니다.',
        ' 도움이 되셨길 바라며, 쾌유를 빕니다.'
    ]
    
    idx_before = randint(0,len(before_sentences)-1)
    idx_after = randint(0,len(after_sentences)-1)

    result = before_sentences[idx_before] + text + after_sentences[idx_after]
    
    return result


def add_link(text):
    dict_link = {'illness':['불면증', '기면증', '렘수면', '가위', 'adhd', '하지불안', '식이장애', '공황장애', '강박증', '특정 공포증', 
                        '알코올 중독', '우울증', '불안장애', '광장공포증', '해리성', '틱', '조현병', '발모광', '수면과다', '정신분열증', '수면위생'], 
             'link':['http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31586', 'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31912', 
                     'http://www.samsunghospital.com/home/healthInfo/content/contenView.do?CONT_SRC_ID=09a4727a800763ea&CONT_SRC=CMS&CONT_ID=6040&CONT_CLS_CD=001020001001', 'http://anam.kumc.or.kr/dept/disease/deptDiseaseInfoView.do?BNO=340&cPage=&DP_CODE=AAPY&MENU_ID=004005', 
                     'http://m.amc.seoul.kr/asan/mobile/healthinfo/disease/diseaseDetail.do?contentId=33888&diseaseKindId=C000006', 'http://www.snuh.org/health/nMedInfo/nView.do?category=DIS&medid=AA000361', 
                     'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31885', 'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31583', 
                     'http://www.good-heart.co.kr/board/view/customer02/21', 'http://www.masteroflove.co.kr/main/sub.html?pageCode=12', 
                     'http://www.samsunghospital.com/home/healthInfo/content/contenView.do?CONT_SRC_ID=09a4727a8000f2c4&CONT_SRC=CMS&CONT_ID=987&CONT_CLS_CD=001020001001', 'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31581', 
                     'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31582', 'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31893', 
                     'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31899', 'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31925', 
                     'http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31578', 'http://m.amc.seoul.kr/asan/mobile/healthinfo/disease/diseaseDetail.do?contentId=31882&diseaseKindId=C000006', 
                     'http://www.sleepclinic.kr/clinic/clinic06_new.php', 'http://anam.kumc.or.kr/dept/disease/deptDiseaseInfoView.do?BNO=338&cPage=&DP_CODE=AAPY&MENU_ID=004005', 
                     'http://www.samsunghospital.com/dept/main/index.do?DP_CODE=SPD&MENU_ID=004']}

    idx_link = []

    for ill in range(len(dict_link['illness'])):
        if dict_link['illness'][ill] in text:
            idx_link.append(ill)
            
    if len(idx_link) == 0:
        pass
    else:
        text = text + '\n'*2 + '진단 관련 링크를 첨부합니다. 아래 링크를 클릭하시면 확인하실 수 있습니다.'
        for lnk in idx_link:
            text = text + '\n' + '[' + dict_link['illness'][lnk] + ']: ' + dict_link['link'][lnk]
    
    return text


def postprocess(text, result_type):
    ### result_type ###
    # 1. sim : similarity result
    # 2. dl : deep learning model result

    if result_type == 'dl':
        text = sentence_split(text)
    text = remove_dup(text)
    text = clean(text)
    text = prep.spell_check(text)
    text = add_sentence(text)
    return add_link(text)