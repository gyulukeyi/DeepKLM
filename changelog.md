# DeepKLM

## library_210207

- Titles are fixed -- now it's no longer a "working" title
- Added a colab version for the on-site demonstration

## library_201206

- Library now organized with folders and better file naming (finally!)
- surprisal.py
    - now you can turn off auto-adding period
    - you can now calculate sentential level surprisal (bert_sentence_surprsial())
    - confusion score is returned by sentence rather than by file

## library_201110

- barplot_creator.py
    - Added to draw bar plot
- DeepKLM.ipynb/DeepKLM-Kor.ipynb
    - Added a cell to draw a bar plot

## library_201105

- surprisal.py
    - Implemented confusion score from Lin et al. (2019)

## library_201023

- ETRI's KorBERT is now removed upon distribution.

## library_200923

- boxplot_creator.py
    - now changes the font according to the environrment
- DeepKLM-Kor.ipynb
    - Added a Korean version of the library.

## library_200922

- surprisal.py
    - Now Bert_token_surprisal RETURNS correct sentence in the tuple in the list
    - Returns the tuple (sentence _with mask_, keyword, surprisal) for better compatiblity with the template.
- DeepKLM.ipynb
    - Added instructions
    - Examples are now actual case scenarios
    - Added a batch processing scenario
- requirements.txt
    - Added xlrd >= 1.0.0 (for boxplot_creator.py)
    - Added pytorch-transformers (for CoLab compatability)
- boxplot_creator.py
    - Simplified
    - Now provided with template.xlsx

## library_200916_2

- surprisal.py 
    - Now Bert_token_suprisal RETURNS a list of tuple containing the sentence and the surprisal info for scalable research
- DeepKLM.ipynb
    - If KorBERT is not available, it will not try to load it

## library_200916

- The library is now changelogged (finally!)
- "surprisal.py" is documentation ready
- The library is ready for ETRI's KorBERT
- KorBERT (and ETRI API key) is temporarily provided -- BE CAREFUL WHEN SHARING THEM. They are not meant to be shared publically!