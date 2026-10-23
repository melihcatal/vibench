import os
import requests
from typing import Dict

# Managed Translation service: Google Cloud Translation API
# Requires GOOGLE_APPLICATION_CREDENTIALS env var pointing to JSON key file.

TRANS_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'

TOKEN = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def detect_language(text: str) -> str:
    """Detect language of supplied text using the API."""
    payload = {'q': text}
    response = requests.post(TRANS_ENDPOINT, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f'Translation detection error: {response.status_code}')
    return response.json()['data']['detections'][0][0]['language']


def translate_text(text: str, target_lang: str = 'es') -> Dict[str, str]:
    """Translate text to target language (default Spanish) and return mapping."""
    payload = {
        'q': text,
        'target': target_lang
    }
    response = requests.post(TRANS_ENDPOINT, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f'Translation error: {response.status_code}')
    translated = response.json()['data']['translations'][0]['translatedText']
    return {'original': text, 'translated': translated, 'language': target_lang}

if __name__ == "__main__":
    # Demo usage
    result = translate_text('Hello, world!', target_lang='fr')
    print('Translation:', result)
