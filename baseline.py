import torch
import librosa
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import pandas as pd
from tqdm import tqdm

ROOT = ''
data = pd.read_csv("test-metadata.csv")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_id="herwoww/nadi2025_task3_B1"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)


pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    device=device
)

def process_audio(row):
    wav, sr = librosa.load(f"{ROOT}/{row['audio_path']}", sr=16000)
    row['predicted_text'] = pipe(wav, generate_kwargs={'num_beams': 10, 'early_stopping': True})['text']
    
    return row

tqdm.pandas()
data = data.progress_apply(process_audio, axis=1)
data.to_csv("test-metadata-baseline.csv", index=False)

print("Done!")