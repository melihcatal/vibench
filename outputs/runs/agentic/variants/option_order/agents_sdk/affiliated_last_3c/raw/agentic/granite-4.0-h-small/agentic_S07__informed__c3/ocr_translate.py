# Translate extracted OCR text using DeepL API
import os
import requests

class DeepLTranslator:
    """DeepL translation helper that uses the DeepL API."""
    def __init__(self):
        self.auth_key = os.getenv('DEEPL_AUTH_KEY')
        if not self.auth_key:
            raise RuntimeError('Set DEEPL_AUTH_KEY environment variable')
        self.endpoint = 'https://api.deepl.com/v2/translate'

    def translate(self, text: str, target_lang: str = 'EN') -> str:
        """Translate `text` into the target language and return the result."""
        params = {
            'auth_key': self.auth_key,
            'text': text,
            'target_lang': target_lang
        }
        resp = requests.post(self.endpoint, data=params)
        resp.raise_for_status()
        data = resp.json()
        return data['translations'][0]['text']
