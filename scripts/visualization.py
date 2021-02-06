#!/usr/bin/env python

"""visualization.py
Functions for visualizing attention
"""

import os
import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import seaborn
import IPython
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from sys import path

path.append(os.path.abspath(os.getcwd())+"/bertviz")
from keras.preprocessing.sequence import pad_sequences
from bertviz import head_view

# 입력 데이터 변환
def convert_input_data(sentences, tokenizer):

    # BERT의 토크나이저로 문장을 토큰으로 분리
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

    # 입력 토큰의 최대 시퀀스 길이
    MAX_LEN = 64

    # 토큰을 숫자 인덱스로 변환
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

    # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # 어텐션 마스크 초기화
    attention_masks = []

    # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
    # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
    for seq in input_ids:
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)

    # 데이터를 파이토치의 텐서로 변환
    inputs = torch.tensor(input_ids, dtype=torch.long)
    masks = torch.tensor(attention_masks, dtype=torch.long)

    return inputs, masks

def attention_heatmap(sentences, model, tokenizer, device, vis_opt=0):

    ## Tokenization
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
    print('input_tokens =', tokenized_texts)

    ## Feedforward
    model.eval() # 평가모드로 변경
    inputs, masks = convert_input_data(sentences, tokenizer) # 문장을 입력 데이터로 변환
    print('input_ids =', inputs.tolist())
    if device == torch.device("cuda"):
        b_input_ids = inputs.to("cuda") # 데이터를 GPU에 넣음
        b_input_mask = masks.to("cuda")
    else:
        b_input_ids = inputs.to("cpu")
        b_input_mask = masks.to("cpu")

    with torch.no_grad():
        outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)

    ## SelfAttentions
    # outputs[-1] == (attentions) # https://github.com/huggingface/transformers/blob/f9f8a5312e92541ff9a5f483fc4907ec87da876e/src/transformers/modeling_bert.py#L1290
    # outputs[-1][-1] == last layer
    # outputs[-1][-1].size() == torch.Size([1, 12, 64, 64]) 'bsz, n_heads, max_len, max_len'
    attention_map = torch.mean(outputs[-1][-1], dim=1) # averaging 12 heads == [1, 64, 64]
    attention_map = attention_map[0] # to consider only one sentence
    numpy_attentions = attention_map.detach().cpu().numpy() # tensor to numpy
    max_len = len(tokenized_texts[0]) # to consider only one sentence
    numpy_attentions = numpy_attentions[0:max_len, 0:max_len] # to exclude unnecessary tokens

    ## Visualization
    if vis_opt == 0:
        seaborn.heatmap(numpy_attentions,
              xticklabels=tokenized_texts[0], yticklabels=tokenized_texts[0],
              square=True, cbar=True)
    elif vis_opt == 1:
        numpy_attentions = np.mean(numpy_attentions, axis=0)
        numpy_attentions = numpy_attentions.reshape((len(numpy_attentions), 1))
        seaborn.heatmap(numpy_attentions,
              yticklabels=tokenized_texts[0], square=True, cbar=True)
    elif vis_opt == 2:
        numpy_attentions = np.mean(numpy_attentions, axis=0)
        numpy_attentions = numpy_attentions.reshape((1, len(numpy_attentions)))
        seaborn.heatmap(numpy_attentions,
              xticklabels=tokenized_texts[0], square=True,
              cbar=True, cbar_kws={
                    "use_gridspec": False,
                    "location": "top"})


def call_html(): #for Colab support of visualize_attention_head()
    display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              "d3": "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.8/d3.min",
              jquery: '//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min',
            },
          });
        </script>
        '''))

def visualize_attention_head(model, tokenizer, sentence_a, sentence_b=None):
    inputs = tokenizer.encode_plus(sentence_a, sentence_b, return_tensors='pt', add_special_tokens=True)
    input_ids = inputs['input_ids']
    if sentence_b:
        token_type_ids = inputs['token_type_ids']
        attention = model(input_ids, token_type_ids=token_type_ids)[-1]
        sentence_b_start = token_type_ids[0].tolist().index(1)
    else:
        attention = model(input_ids)[-1]
        sentence_b_start = None
    input_id_list = input_ids[0].tolist() # Batch index 0
    tokens = tokenizer.convert_ids_to_tokens(input_id_list)
    call_html()

    head_view(attention, tokens, sentence_b_start)
