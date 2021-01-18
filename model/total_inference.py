import os
from model.model import *
from transformers import T5Tokenizer, TFMT5ForConditionalGeneration
import model.dataloader as dtl
from torch.utils.data import (DataLoader, TensorDataset)


class ModelInference:
    def __init__(self):
        self.seq2seq = Seq2Seq()
        self.seq2seq.load_state_dict(
            torch.load(os.path.join('model/seq2seq_ans3cut_epoch_10.pt'), 
            map_location=lambda storage, loc: storage))
        self.seq2seq.eval()


        self.mt5 = TFMT5ForConditionalGeneration.from_pretrained("google/mt5-small")
        self.mt5_tokenizer = T5Tokenizer.from_pretrained('google/mt5-small')
        self.mt5.load_weights('model/t5.h5')
        

    def inference_seq2seq(self,text_token):
        model = self.seq2seq
        model.eval()
        test_datas = dtl.make_dialog_pair(text_token,sentence=True)
        test_input_features, test_output_features = dtl.convert_data2feature(test_datas,128, dtl.word2idx)
        test_features = TensorDataset(test_input_features, test_output_features)
        test_dataloader = DataLoader(test_features, shuffle=False, batch_size=1)
    
        for step, batch in enumerate(test_dataloader):
        
            batch = tuple(t for t in batch)

            # 토큰 데이터, 라벨 데이터
            input_features, output_features = batch[0], batch[1]

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

    def inference_mt5(self,text_token):
        model = self.mt5
        tokenizer = self.mt5_tokenizer

        inputs = tokenizer.prepare_seq2seq_batch(src_texts=text_token,
                                                 return_tensors='tf',
                                                 max_length=128).input_ids
        output = model.generate(inputs,
                            max_length=200,
                            repetition_penalty=20,
                            early_stopping=True,
                            num_beams=10)
        return (tokenizer.decode(output[0]))