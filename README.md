# AM I OK? 
### 전문의 답변 기반 심리진단 AI 🧐
2021.01.16. **[제 11회 투빅스 빅데이터 컨퍼런스](https://user-images.githubusercontent.com/43749571/104812963-447f9180-5849-11eb-8725-7453e129c5e9.jpeg)** 발표작
 
<table>
  <tr>
    <td align="center"><img src="https://user-images.githubusercontent.com/43749571/104812828-48f77a80-5848-11eb-9367-3cce4711f56d.jpeg" width="700px;" alt=""/></a></td>
  </tr>
</table>

* **정신 질환 고민**에 대한 질문글을 남기면, **진단**을 통해 답변을 생성해 주는 서비스입니다. 
* **TextRank**로 질문을 추출 요약하고, **Seq2seq**과 **T5**를 통해 답변을 생성합니다. 
* 네이버 지식iN 전문의 답변을 토대로 구성되었으며, 상업적으로 이용할 의도가 전혀 없음을 밝힙니다. 

<br>


## Usage 
### 1. Environment  
#### 1.1. Create virtual environment 
```sh
$ conda create -n virtualenv
$ conda activate virtualenv
```
#### 1.2. git Clone 
```sh
$ git clone https://github.com/cryingjin/AMIOK.git
$ cd AMIOK
```
### 2. Install Packages & Download Models
#### 2.1. Install Mecab 
##### 2.1.1. Install [mecab-ko](https://bitbucket.org/eunjeon/mecab-ko/downloads/) 
```sh
$ tar xvfz mecab-0.996-ko-0.9.2.tar.gz
$ cd mecab-0.996-ko-0.9.2
$ ./configure
$ make
$ make check
$ sudo make install
```

##### 2.1.2. Install [mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/) 
```sh
$ tar xvfz mecab-ko-dic-2.1.1-20180720.tar.gz
$ cd mecab-ko-dic-2.1.1-20180720
$ ./configure
$ make
$ sudo make install
```

##### 2.1.3. Install mecab-python 
```sh
$ git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
$ cd mecab-python-0.996
$ python setup.py build
$ su
# python setup.py install
```

#### 2.2. Install requirements 
```sh
$ pip install -r requirements.txt
```

#### 2.3. Install py-hanspell 
```sh
$ git clone https://github.com/ssut/py-hanspell.git
$ cd py-hanspell 
$ python setup.py install
```

#### 2.4. Download Data 
[drive](https://drive.google.com/drive/folders/1oMNP5UddryHfpWuiF1tuwuDMI0k9Zp_-?usp=sharing)의 `tr_question_final.pickle`, `tr_answer_final.pickle` 파일을 `AMIOK/data/` 경로에 다운로드 받아주세요. 


#### 2.5. Get Pre-trained Checkpoints 
[drive](https://drive.google.com/drive/u/0/folders/1WxCVWOWGPS2PHhqoGOgnZRu-pkbqCvUw)의 `seq2seq_ans3cut_epoch_10.pt`, `t5.h5` 파일을 `AMIOK/model/` 경로에 다운로드 받아주세요.


### 3. Run! ✨
```sh
$ python main.py -s "질문글을 입력해주세요 :>"
```

<br>

## Results 
<table>
  <tr>
    <td align="center"><img src="https://user-images.githubusercontent.com/43749571/104932863-85afa700-59eb-11eb-8dc0-b8c67aac31fd.jpeg" width="700px;" alt=""/></a></td>
  </tr>
  <tr>
    <td align="center"><img src="https://user-images.githubusercontent.com/43749571/104932880-89432e00-59eb-11eb-94e7-74179adf0aba.jpeg" width="700px;" alt=""/></a></td>
  </tr>
  <tr>
    <td align="center"><img src="https://user-images.githubusercontent.com/43749571/104932884-8a745b00-59eb-11eb-97c8-5a7dd048dfa7.jpeg" width="700px;" alt=""/></a></td>
  </tr>
</table>



<br>

## Presentation
저희 프로젝트에 대해 자세하게 알고 싶으시다면, 하단의 링크를 참고해주세요! 
* [![GoogleDrive Badge](https://img.shields.io/badge/REPORT-405263?style=flat-square&logo=Quip&link=https://drive.google.com/file/d/1VnYsB8k4Fxu6UFhAxuTi4m01BjoH2uwS/view?usp=sharing)](https://drive.google.com/file/d/1VnYsB8k4Fxu6UFhAxuTi4m01BjoH2uwS/view?usp=sharing)
* [![Youtube Badge](https://img.shields.io/badge/Youtube-ff0000?style=flat-square&logo=youtube&link=https://youtu.be/KPS1sD_lcMc)](https://youtu.be/KPS1sD_lcMc)



<br>

## Contributors 🐻
빅데이터 동아리 **[ToBig's](http://www.datamarket.kr/xe/)** 멤버들이 함께한 프로젝트입니다.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable --> 

<table>
  <tr>
    <td align="center"><a href="https://github.com/jhtobigs"><img src="https://user-images.githubusercontent.com/43749571/104813217-231fa500-584b-11eb-9e58-90460f99c15b.png" width="150" height="150"><br /><sub><b>Juho Kim</b></sub></td>
    <td align="center"><a href="https://github.com/gyeong707"><img src="https://user-images.githubusercontent.com/43749571/104813219-23b83b80-584b-11eb-856f-6d3de4ed1335.JPG" width="150" height="150"><br /><sub><b>Migyeong Kang</b></sub></td>
    <td align="center"><a href="https://github.com/kmmnjng528"><img src="https://user-images.githubusercontent.com/43749571/104813221-2450d200-584b-11eb-986e-328f2ebf43c2.JPG" width="150" height="150"><br /><sub><b>Minjeong Kim</b></sub></td>
    <td align="center"><a href="https://github.com/cryingjin"><img src="https://user-images.githubusercontent.com/43749571/104813223-24e96880-584b-11eb-96b8-dfe4de1b0274.png" width="150" height="150"><br /><sub><b>Yejin Lee</b></sub></td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><a href="https://github.com/jbeen2"><img src="https://user-images.githubusercontent.com/43749571/104813215-21ee7800-584b-11eb-8958-9f407108ff0c.jpeg" width="150" height="150"><br /><sub><b>Jaebeen Lee</b></sub></td>
    <td align="center"><a href="https://github.com/placidmoon1"><img src="https://user-images.githubusercontent.com/43749571/104813213-1e5af100-584b-11eb-9d52-6af880788410.jpg" width="150" height="150"><br /><sub><b>Guhong Min</b></sub></td>
    <td align="center"><a href="https://github.com/Jieun-Enna"><img src="https://user-images.githubusercontent.com/43749571/104813218-231fa500-584b-11eb-868b-b7c0f7ce30c7.jpg" width="150" height="150"><br /><sub><b>Jieun Park</b></sub></td>
    <td align="center"><a href="https://github.com/hrlee113"><img src="https://user-images.githubusercontent.com/43749571/104813214-1f8c1e00-584b-11eb-93f2-cd0e8a195713.jpeg" width="150" height="150"><br /><sub><b>Hyerin Lee</b></sub></td>
  </tr>
</table>
