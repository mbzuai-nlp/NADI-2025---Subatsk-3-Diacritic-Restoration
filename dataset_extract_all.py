import os
from datasets import load_dataset
import pandas as pd
import shutil
from pydub import AudioSegment
import numpy as np
from tqdm import tqdm

dataset_name = "MBZUAI/NADI-2025-Sub-task-3-all"
# ---- CONFIGURE THESE ----
config = None
output_dir = "output"
save_format = "csv"
# -------------------------


import pyarabic.araby as araby

def remove_diacritics(row):
    row['text'] = araby.strip_diacritics(row['text'])
    return row

import string
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

# Load dataset
if config:
    ds = load_dataset(dataset_name, config)
else:
    ds = load_dataset(dataset_name)

splits = ['dev']
os.makedirs(output_dir, exist_ok=True)

for split in splits:
    if split not in ds:
        print(f"Split '{split}' not found in dataset.")
        continue
    split_dir = os.path.join(output_dir, split)
    os.makedirs(split_dir, exist_ok=True)

    audios_dir = os.path.join(split_dir, dataset_name.split("/")[1], "audios")
    os.makedirs(audios_dir, exist_ok=True)

    processed_data = []
    for i, item in tqdm(enumerate(ds[split])):
        audio_dict = item['audio']
        audio_data_float = audio_dict['array']
        sampling_rate = audio_dict['sampling_rate']
        text = item['transcription']
        
        original_filename = item.get('file', f"audio_{i}.wav")
        audio_filename = os.path.basename(original_filename)
        if not audio_filename.lower().endswith(".wav"):
            audio_filename += ".wav"
            
        audio_path = os.path.join(audios_dir, audio_filename)
        
        try:
            audio_data_int = (audio_data_float * 32767).astype(np.int16)
            audio_segment = AudioSegment(
                data=audio_data_int.tobytes(),
                sample_width=audio_data_int.dtype.itemsize,
                frame_rate=sampling_rate,
                channels=1
            )
            audio_segment.export(audio_path, format="wav")
        except Exception as e:
            print(f"Error processing audio file {audio_filename}: {e}")
            continue
            
        relative_audio_path = os.path.join(split, dataset_name, "audios", audio_filename)
        processed_data.append({"audio_path": relative_audio_path, "text": text})

    df = pd.DataFrame(processed_data)
    
    if True:
        df = df.apply(remove_diacritics, axis=1)
    
    df['text'] = df['text'].apply(remove_punctuation)
    save_path = os.path.join(split_dir, f"{split}-metadata.{save_format}")
    
    if save_format == "csv":
        df.to_csv(save_path, index=False)
    elif save_format == "json":
        df.to_json(save_path, orient="records", lines=True)
    elif save_format == "tsv":
        df.to_csv(save_path, sep="\\t", index=False)
    print(f"Saved {split} split to {save_path}")

    # zip_name = os.path.join(output_dir, f"{split}_split")
    # shutil.make_archive(zip_name, 'zip', split_dir)
    # print(f"Compressed {split} split folder to {zip_name}.zip")

print("Done!")
