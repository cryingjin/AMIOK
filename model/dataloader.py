from torch.utils.data import (DataLoader, TensorDataset)
import pickle5 as pickle
import numpy as np
import torch

'''
word_dict utils
word2idx, idx2word
'''
with open( 'data/ypos_word2idx.pickle', 'rb') as f:   
    word2idx = pickle.load(f)
with open('data/ypos_idx2word.pickle', 'rb') as f:   
    idx2word = pickle.load(f)
    
    
'''
dataloader utils
'''
def make_dialog_pair(question, answer=None, sentence=False):
    '''
    질문, 답변이 token으로 된 리스트를 받아서 pair를 튜플로 만든다
    Args :
        question : 문장별 token list 
        answer : 문장별 token list
        sentence : inference 용 한 문장을 받을 경우 sentence=True
    Returns : 
        [(q1,a1),...]
    '''

    if sentence == True:
        pairs = [(question, list())]
    else:
        pairs = []
        if answer is None:
            for i in range(len(question)):
                pairs.append((question[i], list()))
        
        else:
            for i in range(len(question)):
                pairs.append((question[i], answer[i]))
    
    return pairs
    

def convert_data2feature(datas, max_length, word2idx):
    '''token데이터를 feature로 변환한다'''
    
    input_features, output_features = [], []
    for input_sequence, output_sequence in (datas):

        input_feature, output_feature = np.zeros(shape=(max_length), dtype=np.int), np.zeros(shape=(max_length), dtype=np.int)

        # 입력 sequence의 각 값들을 index로 치환하고 위에서 생성한 numpy array에 저장
        for index in range(len(input_sequence[:max_length-1])):
            try:
                input_feature[index] = word2idx[input_sequence[index]]
            except:  # unknown
                input_feature[index] = word2idx['<UNK>']

        # 출력 sequence의 각 값들을 index로 치환하고 위에서 생성한 numpy array에 저장
        for index in range(len(output_sequence[:max_length-1])):
            try:
                output_feature[index] = word2idx[output_sequence[index]]
            except:
                output_feature[index] = word2idx['<UNK>']
        
        # 출력 sequence의 마지막 부분에 <EOS> 추가
        output_feature[index+1] = word2idx["<EOS>"]    
        
        # 변환한 데이터를 각 리스트에 저장
        input_features.append(input_feature)
        output_features.append(output_feature)

    # 변환한 데이터를 Tensor 객체에 담아 반환
    input_features = torch.tensor(input_features, dtype=torch.long)
    output_features = torch.tensor(output_features, dtype=torch.long)

    return input_features, output_features      
   
