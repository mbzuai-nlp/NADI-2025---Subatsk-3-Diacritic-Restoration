import pandas as pd


def remove_diacritics_except_allowed(text):
    """
    Remove Arabic diacritics from text except for allowed ones based on the provided list
    
    Keeps only: Shaddah (ّ), Kasra (ِ), and Shaddah+Kasra combinations (ِّ)
    
    Args:
        text (str): Arabic text with diacritics
        
    Returns:
        str: Text with only allowed diacritics preserved
    """
    
    # Define the allowed diacritics based on the provided list
    allowed_diacritics = {
        'ِ',    # Kasra
        'ّ',    # Shaddah  
        # 'ِّ',   # Shaddah + Kasra
    }
    
    # Define all Arabic diacritics to potentially remove
    all_diacritics = {
        'َ',    # Fatha
        'ً',    # Fathatah
        'ُ',    # Damma
        'ٌ',    # Dammatan
        'ِ',    # Kasra (keep)
        'ٍ',    # Kasratan
        'ْ',    # Sukun
        'ّ',    # Shaddah (keep)
        'َّ',   # Shaddah + Fatha
        'ًّ',   # Shaddah + Fathatah
        'ُّ',   # Shaddah + Damma
        'ٌّ',   # Shaddah + Dammatan
        'ِّ',   # Shaddah + Kasra (keep)
        'ٍّ',   # Shaddah + Kasratan
    }
    
    # Create a set of diacritics to remove
    diacritics_to_remove = all_diacritics - allowed_diacritics
    
    # Remove unwanted diacritics
    cleaned_text = text
    # Sort by length (longest first) to handle compound diacritics properly
    for diacritic in sorted(diacritics_to_remove, key=len, reverse=True):
        cleaned_text = cleaned_text.replace(diacritic, '')
    
    return cleaned_text

TEXT = 'predicted_text'
data = pd.read_csv('test-metadata-baseline.csv')
# data[TEXT] = data[TEXT].apply(remove_diacritics_except_allowed)
data[[TEXT]].to_csv('predictions.txt', index=False, header=None)