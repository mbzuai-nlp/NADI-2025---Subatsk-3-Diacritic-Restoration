import os
import sys
import zipfile
import traceback # For detailed error trace
import subprocess

from evaluate import load
wer = load('wer')


try:
    from diacritization_evaluation import der
except ImportError as e:
    print(f"Failed to import diacritization_evaluation: {e}", file=sys.stderr) # Kept
    print("Please ensure 'diacritization_evaluation' is in requirements.txt and installed.", file=sys.stderr) # Kept
    sys.exit(1)

def calculate_scores(reference_file_path, prediction_file_path, use_case_ending=True):
    if reference_file_path is None or prediction_file_path is None:
        print(f"ERROR in calculate_scores: Reference or Prediction file path is None. REF='{reference_file_path}', PRED='{prediction_file_path}'", file=sys.stderr); sys.stderr.flush() # Kept
        return -1.0, -1.0
    
    try:
        with open(reference_file_path, encoding="utf8") as file:
            original_content = file.read()

        with open(prediction_file_path, encoding="utf8") as file:
            predicted_content = file.read()

        der_score = der.calculate_der(original_content, predicted_content)
        # wer_score = wer.calculate_wer(original_content, predicted_content)
        wer_score = wer.compute(references=original_content.split('\n'), predictions=predicted_content.split('\n'))
        wer_score = round(wer_score, 2)
       
        return der_score, wer_score
    except Exception as e:
        print(f"ERROR in calculate_scores: {e}", file=sys.stderr) # Kept
        print(traceback.format_exc(), file=sys.stderr) # Kept
        return -1.0, -1.0

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python score.py <reference> <predictions>. Received {len(sys.argv)} args: {sys.argv}", file=sys.stderr) # Kept
        sys.exit(1)

    actual_reference_file = sys.argv[1]
    predicted_file_path = sys.argv[2]

    der_score, wer_score = calculate_scores(actual_reference_file, predicted_file_path)
    
    print(f"der: {der_score}")
    print(f"wer: {wer_score}")
   