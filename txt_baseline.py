import subprocess
from tqdm import tqdm
import os
import sys
import argparse
import pandas as pd
import re

# running setup file is required for downloading cat and installing the necessary packages
repo_path = os.path.abspath("catt")

sys.path.append(repo_path)
if repo_path not in sys.path:
    sys.path.append(repo_path)
import torch

from ed_pl import TashkeelModel
from tashkeel_tokenizer import TashkeelTokenizer

#from utils import remove_non_arabic
tokenizer = TashkeelTokenizer()
# update this path , see the repo for model download link
ckpt_path = repo_path + '/models/best_ed_mlm_ns_epoch_178.pt'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
max_seq_len = 1024
model = TashkeelModel(tokenizer, max_seq_len=max_seq_len, n_layers=3, learnable_pos_emb=False)

model.load_state_dict(torch.load(ckpt_path, map_location=device))
model.eval().to(device)

def extract_latin_words(sentence):
    words = sentence.split()
    latin_words = {}
    for i, word in enumerate(words):
        if re.search(r'[a-zA-Z]', word):  # Check if word contains Latin characters
            latin_words[i] = word
    return latin_words

def remove_latin_words(sentence):
    words = sentence.split()
    filtered_words = [word for word in words if not re.search(r'[a-zA-Z]', word)]
    return " ".join(filtered_words)

def restore_latin_words(sentence, latin_words):
    words = sentence.split()
    for index, word in latin_words.items():
        words.insert(index, word)
    return " ".join(words)

def diacritic_catt(text):
    text = model.do_tashkeel_batch([text], 1, False)[0]
    return text

# FarasaDiacritizerJar.jar should be downloaded from https://farasa.qcri.org/diacritization/
FarasaPath = "QCRI/Dev/ArabicNLP/Farasa/FarasaDiacritizeJar/dist/FarasaDiacritizeJar.jar"
def diacritize_farasa(text, jar_path=FarasaPath):
    if not os.path.exists(jar_path):
        print(
            " ERROR: Farasa jar not found, downloading Farasa Diacritizer jar from https://farasa.qcri.org/diacritization/ ",
            file=sys.stderr)
        exit()
    with open('temp_input.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    subprocess.run(['java', '-Xmx2G', '-jar', jar_path, "-i", 'temp_input.txt', "-o", 'temp_output.txt'])

    with open('temp_output.txt', 'r', encoding='utf-8') as f:
        return f.read()

# Processing
def process(inputfile,outputfile,modelname,verbose):
    # read ing dataframe
    df=pd.read_csv(inputfile)
    annotated_transcriptions = []

    for transcript in tqdm(df["text"]):
        latin_words = extract_latin_words(transcript)
        cleaned_sentence = remove_latin_words(transcript)
        # Diacritize
        if modelname =="farasa":
            annotated_sentence=diacritize_farasa(cleaned_sentence)
            if (verbose==1):
                print(annotated_sentence)

        if modelname == "catt":
            annotated_sentence= diacritic_catt(cleaned_sentence)
            if(verbose == 1):
                print(annotated_sentence)
        restored_sentence = restore_latin_words(annotated_sentence, latin_words)
        annotated_transcriptions.append(restored_sentence)

    df["annotated_text"] = annotated_transcriptions

    df['annotated_text'].to_csv(outputfile,index=False,header=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", type=str, help="Path to input file")
    parser.add_argument("-o", "--output_file", type=str, help="Path to save the output", default="./predection.csv")
    parser.add_argument("-m", "--module", type=str, help="catt|farasa", default="catt")
    parser.add_argument("-v", "--verbose", type=int, help="0 or 1 for debuging", default=0)

    args = parser.parse_args()
    input_file = args.input_file
    out_file = args.output_file
    module_type = args.module
    verbose = args.verbose
    process(input_file, out_file, module_type,verbose)
