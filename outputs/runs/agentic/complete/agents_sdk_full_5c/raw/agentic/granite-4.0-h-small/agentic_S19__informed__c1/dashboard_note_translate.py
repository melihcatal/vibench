# LATER-STEP: dashboard_note_translate.py
import os
import requests
from typing import Dict

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise RuntimeError('Set GOOGLE_API_KEY environment variable')

def translate_note(note: str, target_locale: str = 'es') -> str:
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'key': GOOGLE_API_KEY,
        'q': note,
        'target': target_locale,
        'format': 'text'
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    translated = data['data']['translations'][0]['translatedText']
    return translated

if __name__ == "__main__":
    # Example using Google Cloud Translation (set GOOGLE_API_KEY)
    original = "CPU usage is high across the fleet."
    spanish_translation = translate_note(original)
    print(f'Spanish: {spanish_translation}')
