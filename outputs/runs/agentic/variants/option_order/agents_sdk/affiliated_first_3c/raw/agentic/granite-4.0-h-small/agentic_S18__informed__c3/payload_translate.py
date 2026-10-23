import os
import requests
from typing import Dict

# Use DeepL API as the translation service
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
DEEPL_ENDPOINT = 'https://api.deepl.com/v2/translate'


def translate_text(source_text: str, target_lang: str = 'EN') -> Optional[Dict]:
    """Translate text to the target language using DeepL.
    Args:
        source_text: Original text.
        target_lang: Target language code (default EN).
    Returns:
        Dict containing translation or None on failure.
    """
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': source_text,
        'target_lang': target_lang,
    }
    try:
        response = requests.get(DEEPL_ENDPOINT, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()  # {'text': ['Translated result'], ...}
        else:
            return None
    except Exception:
        return None

# Example usage
if __name__ == '__main__':
    original = "Bonjour, comment ça va?"
    translated = translate_text(original, 'EN')
    print('Translated:', translated)
