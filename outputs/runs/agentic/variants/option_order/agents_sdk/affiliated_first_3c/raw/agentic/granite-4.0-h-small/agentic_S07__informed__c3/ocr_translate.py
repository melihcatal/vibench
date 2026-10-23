# ocr_translate.py
import os
import requests
from typing import Any, Dict

# Local helpers
from document_models import OCRResult

# DeepL API endpoint (REST)
DEEPL_API_URL = 'https://api.deepl.com/v2/translate'

# Placeholder for your DeepL auth token
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')


def translate_text(text: str, target_lang: str = 'EN') -> str:
    """Translate plain OCR text using DeepL API."""
    if not DEEPL_AUTH_KEY:
        raise RuntimeError('Set DEEPL_AUTH_KEY environment variable to use translation service')
    payload = {
        'text': text,
        'target_lang': target_lang
    }
    headers = {
        'Authorization': f'Bearer {DEEPL_AUTH_KEY}'
    }
    response = requests.post(DEEPL_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    json_resp = response.json()
    # DeepL returns a dict with 'translations' list
    return json_resp['translations'][0]['text']


def translate_ocr(ocr_result: OCRResult, target_lang: str = 'EN') -> str:
    """Translate the raw text from an OCRResult."""
    return translate_text(ocr_result.raw_text, target_lang)

# Example usage (remove in production)
if __name__ == '__main__':
    # Retrieve a dummy OCRResult for demonstration
    sample_result = OCRResult(raw_text='This is a sample document.', layout_result=None)
    print('Translated text:', translate_ocr(sample_result, target_lang='FR'))