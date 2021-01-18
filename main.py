import prep.preprocess as prep
import prep.data as dt
import prep.tokenizer as tk
import trpkg.textrank as tr
import sim.similarity as sim 
import post.postprocess as post
import argparse
import model.inference as seq
from model.total_inference import *

if __name__ == '__main__':
    inferencer = ModelInference()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', help="input_sentence", nargs='+', required=True)
    args = parser.parse_args()
    sentence = args.s[0]
    print("\n[Input sentence]", sentence)

    # preprocess
    sentence = prep.preprocess(sentence)
    print("\n[modified sentence]", sentence)

    # textrank
    sentence = tr.sentence_extraction(sentence)
    print("\n[textrank result]", sentence)

    # tokenizing
    npo, ypo = tk.mecab_tokenizer(sentence)

    ##### 어떤 모델을 쓸까? #####
    # similarity
    result_type = 'sim'
    answer = sim.output(ypo)

    if answer == "No Result":
        if len(sentence) <= 200:
            answer = inferencer.inference_seq2seq(ypo)
            result_type = 'dl'
        else:
            print("가랏 티파니")
            answer = inferencer.inference_mt5(sentence)
            result_type = 'dl'

    # postprocess
    answer = post.postprocess(answer, result_type)
    print("\n[",result_type, "answer ]", answer)