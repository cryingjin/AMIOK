from torch.utils.data import (DataLoader, TensorDataset)
# from model import *    # 같은 model 폴던 안에 있음
# from dataloader import *
import model.model as seq
import model.dataloader as dtl
import torch
import os

def inference(text_token):
    # 평가 데이터 읽기
    test_datas = dtl.make_dialog_pair(text_token,sentence=True)

    # word_dict load -> dataloader에서 
    # word2idx, idx2word
    test_input_features, test_output_features = dtl.convert_data2feature(test_datas,128, dtl.word2idx)

    # 평가 데이터를 batch 단위로 추출하기 위한 DataLoader 객체 생성
    test_features = TensorDataset(test_input_features, test_output_features)
    test_dataloader = DataLoader(test_features, shuffle=False, batch_size=1)
    # Seq2Seq 모델 객체 생성
    model = seq.Seq2Seq()#.cuda()
    # 사전학습한 모델 파일로부터 가중치 불러옴
    model.load_state_dict(torch.load(os.path.join('model/seq2seq_ans3cut_epoch_10.pt' ), map_location=lambda storage, loc: storage))  # config["output_dir_path"]
    # evaluation
    model.eval()
    
    for step, batch in enumerate(test_dataloader):
        # batch = tuple(t.cuda() for t in batch)
        batch = tuple(t for t in batch)

        # 토큰 데이터, 라벨 데이터
        input_features, output_features = batch[0], batch[1]
        # print('input_features : ',input_features)
        # print('output_features : ',output_features)

        with torch.no_grad():
            predicts = model(input_features)
    
        predicts, input_features = predicts[0], input_features[0]
        
        # Tensor를 리스트로 변경
        predicts = predicts.cpu().numpy()
        label_idx = output_features.squeeze().cpu().numpy()   # tensor 조작
    
    # 바꿔도됨
    answer = ''
    for idx in predicts.tolist():
        word = dtl.idx2word[idx][0]  # 형태소 토큰만

        if(word == "<EOS>"):
            break

        answer += word 
    # print(answer)

    return answer