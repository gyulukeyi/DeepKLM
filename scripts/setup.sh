#!/bin/bash

# Installing libraries
echo "Installing required packages"
pip3 install -r ./scripts/requirements.txt
echo "Done!"

# Fetch needed files
echo "Cloning from GitHub"
git clone https://github.com/snunlp/KR-BERT.git
git clone https://github.com/jessevig/bertviz.git
echo "Done!"
echo "Getting the pretrained model"
if [ -f "./KR-BERT/krbert_pytorch/pretrained/pytorch_model_char16424_bert.bin" ]; then
    echo "BERT tokenizer character model already exists!"
else
    gdown https://drive.google.com/u/0/uc?id=18lsZzx_wonnOezzB5QxqSliA2KL5BF0x
fi
if [ -f "./KR-BERT/krbert_pytorch/pretrained/pytorch_model_char16424_ranked.bin" ]; then
    echo "BidirectionalWordPeiece tokenizer character model already exists!"
else
    gdown https://drive.google.com/u/0/uc?id=1C87CCHD9lOQhdgWPkMw_6ZD5M2km7f1p
fi
mv pytorch_model_char16424_*.bin ./KR-BERT/krbert_pytorch/pretrained 2>/dev/null
echo "Done!"
