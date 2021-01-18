import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class Decoder(nn.Module):
    def __init__(self, embedding):
        super(Decoder, self).__init__()
        
        self.embedding_size = 128
        self.hidden_size = 128
        self.vocab_size = 36294    # len(word2idx)

        self.embedding = embedding
        self.dropout = nn.Dropout(0.3)

        # GRU layer
        self.gru = nn.GRU(input_size=self.embedding_size, hidden_size=self.hidden_size, num_layers=1) 
        self.linear_1 = nn.Linear(in_features=self.hidden_size*2, out_features=self.hidden_size)
        self.linear_2 = nn.Linear(in_features=self.hidden_size, out_features=self.vocab_size)


    def forward(self, input, last_hidden, encoder_outputs):
        # (batch_size, 1) -> (1, batch_size, embedding_size)
        embedded = self.embedding(input).unsqueeze(0)  # (1,B,N)
        embedded = self.dropout(embedded)

        # rnn_output : (1, batch_size, hidden_size)
        # hidden : (1, batch_size, hidden_size)
        # gru -> output, hidden 나옴
        rnn_output, hidden = self.gru(embedded, last_hidden)      
        rnn_output_for_attention = rnn_output.transpose(0, 1).contiguous()
        encoder_outputs = encoder_outputs.permute(1, 2, 0)

        # attention
        attn_weights = rnn_output_for_attention.bmm(encoder_outputs)
        attn_weights = F.softmax(attn_weights, dim=-1)

        # (batch_size, 1, curr_max_length) * (batch_size, curr_max_length, hidden_size) 
        # -> (batch_size, 1, hidden_size)
        context = attn_weights.bmm(encoder_outputs.transpose(1, 2))
        rnn_output, context = rnn_output.squeeze(0), context.squeeze(1)  # 차원 맞춤

        # (batch_size, hidden_size*2)
        concat_input = torch.cat(tensors=(rnn_output, context), dim=-1)

        # (batch_size, hidden_size*2) -> (batch_size, hidden_size)
        # linear_1 : hidden 사이즈 크기
        concat_output = torch.tanh(self.linear_1(concat_input))

        # (batch_size, hidden_size) -> (batch_size, vocab_size)
        output = self.linear_2(concat_output)

        return output, hidden


# -------------------------------------- Encoder -------------------------------------------
class Seq2Seq(nn.Module):
    def __init__(self):
        super(Seq2Seq, self).__init__()

        self.vocab_size = 36294    # len(word2idx) 
        self.embedding_size = 128
        self.hidden_size = 128
        self.max_length = 128

        self.word_embedding = nn.Embedding(num_embeddings=self.vocab_size,
                                           embedding_dim=self.embedding_size,
                                           padding_idx=0)
        # Bi-GRU layer
        self.bi_gru_1 = nn.GRU(input_size=self.embedding_size,
                             hidden_size=self.hidden_size // 2, 
                             num_layers=1,
                             bidirectional=True)
        self.bi_gru_2 = nn.GRU(input_size=(self.hidden_size),
                             hidden_size=self.hidden_size // 2, 
                             num_layers=1,
                             bidirectional=True)
        # Decoder layer
        self.decoder = Decoder(self.word_embedding)
        self.dropout = nn.Dropout(0.3)


    def forward(self, input_features, output_features=None):
        batch_size = input_features.size()[0]

        input_feature_lengths = (input_features != 0).sum(dim=-1)      # 패딩아닌것 열을 제거

        # (batch_size, max_length) -> (batch_size, max_length, embedding_size)
        input_features = self.word_embedding(input_features)
        input_features = input_features.transpose(0, 1)

        # -------------------------------------- Add Encoder Input -------------------------------------------
        # gru1
        packed_input_features = pack_padded_sequence(input_features, input_feature_lengths.cpu(), batch_first=False, enforce_sorted=False)
        packed_gru_outputs, gru_hidden_states = self.bi_gru_1(packed_input_features)
        gru_outputs_unpacked, input_lengths_unpacked = pad_packed_sequence(packed_gru_outputs, batch_first=False)
        # (배치크기, 문장의 최대 길이, 히든크기)
        # gru1 output + embedding  -> residual net 차용
        new_input = torch.cat([input_features, gru_outputs_unpacked], dim=0)      
        final_input_features = pack_padded_sequence(new_input, input_feature_lengths.cpu(), batch_first=False, enforce_sorted=False)
        # gru2
        packed_gru_outputs, gru_hidden_states = self.bi_gru_2(final_input_features)   
        gru_outputs_unpacked, input_lengths_unpacked = pad_packed_sequence(packed_gru_outputs, batch_first=False)

        # (2, batch_size, hidden_size/2) -> (batch_size, hidden_size)
        gru_hidden_states = torch.cat(tensors=(gru_hidden_states[0], gru_hidden_states[1]), dim=-1)

        # gru_outputs_unpacked : (curr_max_length, batch_size, hidden_size)
        # gru_hidden_states : (batch_size, hidden_size)
        gru_outputs_unpacked, gru_hidden_states = self.dropout(gru_outputs_unpacked), self.dropout(gru_hidden_states)
    
        # -------------------------------------- Decoder Input -------------------------------------------
        # (batch_size, ), 디코더의 시작 step 입력 값을 <SOS> 초기화
        decoder_input = torch.ones(size=(batch_size, ), dtype=torch.long)#.cuda()
        # (batch_size, hidden_size) -> (1, batch_size, hidden_size)
        decoder_hidden = gru_hidden_states.unsqueeze(0)   # 차원
        
        decoder_outputs = []
        
        # train
        if(output_features is not None):
            for step in range(self.con):
                # decoder_output : (batch_size, vocab_size)
                # decoder_hidden : (1, batch_size, hidden_size)
                decoder_output, decoder_hidden = self.decoder(decoder_input, 
                                                              decoder_hidden, 
                                                              gru_outputs_unpacked)

                decoder_input = output_features[:, step]     # decoder outputs 을 batch size 만큼 다음 state 에 넣기 위함
                decoder_outputs.append(decoder_output)

            # (max_length, batch_size, vocab_size)
            decoder_outputs = torch.stack(tensors=decoder_outputs, dim=0)    
            # 각각 분류되어 있는 리스트 형식이기 때문에 stack으로 합쳐줘야함

            # (max_length, batch_size, vocab_size) -> (batch_size, max_length, vocab_size)
            decoder_outputs = decoder_outputs.transpose(0, 1)

            loss_fct = nn.CrossEntropyLoss()

            decoder_outputs = decoder_outputs.reshape(shape=(-1, self.vocab_size))
            output_features = output_features.flatten()

            loss = loss_fct(decoder_outputs, output_features)

            return loss
        
        # test
        else:      
            for t in range(self.max_length):    # self.max_length
                # decoder_output : (batch_size, vocab_size)
                # decoder_hidden : (1, batch_size, hidden_size)
                decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, gru_outputs_unpacked)

                # (batch_size, vocab_size) -> (batch_size, )
                decoder_input = decoder_output.argmax(dim=-1)
                decoder_outputs.append(decoder_output.argmax(dim=-1))       

            # (max_length, batch_size, vocab_size)
            decoder_outputs = torch.stack(tensors=decoder_outputs, dim=0)
            # (batch_size, max_length, vocab_size)
            decoder_outputs = decoder_outputs.transpose(0, 1)

            return decoder_outputs