import requests

from speech_models import normalize_text


def translate_script(text: str, target_language: str = 'en') -> str:
    payload = {'q': normalize_text(text), 'source': 'auto', 'target': target_language, 'format': 'text'}
    response = requests.post('https://translation.googleapis.com/language/translate/v2', params={'key': __import__('os').getenv('GOOGLE_TRANSLATE_API_KEY', '')}, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data['data']['translations'][0]['translatedText']
