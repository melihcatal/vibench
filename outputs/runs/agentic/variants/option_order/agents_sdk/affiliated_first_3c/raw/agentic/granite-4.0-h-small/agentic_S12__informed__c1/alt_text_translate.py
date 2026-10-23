import os
import requests
# Using Google Cloud Translation as example; credentials via GOOGLE_APPLICATION_CREDENTIALS
url = 'https://translation.googleapis.com/language/translate/v2'

def translate_text(text: str, target_lang: str = 'es') -> str:
    """Translate a string (e.g., image description) to another language.

    Returns translated text.
    """
    params = {
        'q': text,
        'target': target_lang,
        'format': 'text'
    }
    response = requests.post(url, data=params)
    result = response.json()
    return result['data']['translations'][0]['translatedText']
