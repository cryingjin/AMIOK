#import config
import os 
import pandas as pd
import pickle5 as pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# =================================
#           Data Load
# =================================

QUESTION_DIR = 'data/tr_question_final.pickle'
ANSWER_DIR = 'data/tr_answer_final.pickle'


# question
with open(os.path.join(QUESTION_DIR), 'rb') as f:
    q = pickle.load(f)

# answer
with open(os.path.join(ANSWER_DIR), 'rb') as f:
    a = pickle.load(f)



def result_df(q, a) :
    qna = pd.DataFrame({
        'question': q['origin'], 'question_tk' : q['ypos'] , 'answer': a['origin']
    })

    pos = ["NNG","NNP",'NNB','NNBC',   # 명사
           "VV","VA",'VV+EP','VV+EC'   # 동사
           ]

    qna["question_tk"] = qna["question_tk"].apply(lambda x: [t for (t, p) in x if p in pos])

    return qna


def pos_remove(ypo) :
    # 특정 품사만 가지고 체크 !
    pos = ["NNG","NNP",'NNB','NNBC',   # 명사
           "VV","VA",'VV+EP','VV+EC'   # 동사
           ]

    npo = [[t for (t, p) in ypo if p in pos]]

    return npo


# =================================
#       Jaccard Similarity
# =================================

def jaccard_score(input1, input2):
    '''
    자카드 유사도 함수
    Args :
        input 으로 input1, input2 를 리스트 형태로 받는다
        토큰으로 된 유사도를 넣는다
    Return:
        자카드 유사도
    '''

    mom = set(input1).union(set(input2))
    son = set(input1).intersection(set(input2))

    return len(son) / len(mom)



def Jaccard_Similarity(data, npo, num) :
    '''
    Args:
        npo : input sentence tokenize
        num : 유사도 개수

    Return:
        jaccard similarity 높은 순서대로 정렬된 dataframe
    '''

    # dataframe
    question, answer = data['question'], data['answer']

    # jaccard similarity
    data["jaccard_similarity"] = data["question_tk"].apply(lambda x : jaccard_score(x, npo[0]))

    # return dataframe
    return data[["question", "answer", "question_tk", "jaccard_similarity"]].sort_values(['jaccard_similarity'], ascending=False)[:num]



# =================================
#       Cosine Similarity
# =================================

# tokenizing 또 할 필요 없으니 함수 만들어서 그대로 사용!
def tokenized_output(tokens):
    return tokens


def Cosine_Similarity(data, npo, num):
    '''
    Args:
        npo : input sentence tokenize
        num : 유사도 개수

    Return:
        cosine similarity 높은 순서대로 정렬된 dataframe
    '''

    question, answer, question_tk = data['question'], data['answer'], data["question_tk"]

    # tf-idf
    vectorizer = TfidfVectorizer(analyzer='word',
                                 tokenizer=tokenized_output,
                                 preprocessor=tokenized_output,
                                 token_pattern=None)

    tfidf_matrix = vectorizer.fit_transform(question_tk)
    question_matrix = vectorizer.transform(npo)

    # cosine similarity
    cos_sim = linear_kernel(tfidf_matrix, question_matrix)
    data["cosine_similarity"] = cos_sim.reshape(-1, )

    return data[["question", "answer", "jaccard_similarity", "cosine_similarity"]].sort_values(['cosine_similarity'], ascending=False)[:num]



# =================================
#            Output
# =================================
def output(ypo) :
    npo = pos_remove(ypo)

    data = result_df(q, a)
    data = Jaccard_Similarity(data, npo, 100)
    data = Cosine_Similarity(data, npo, 50)
    data = data[data["cosine_similarity"] > 0.6].reset_index()

    if len(data) >= 1 :
        output = data["answer"][0]
        
    else : 
        output = 'No Result'

    return output