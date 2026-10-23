import os, json, requests
from observability_models import SimpleLogMsg
from typing import List

# Provider: DeepL API (REST)
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
BASE_URL = 'https://api.deepl.com/v2/translate'
SOURCE_LANG = 'en'   # source language
TARGET_LANG = 'es'   # destination language

def translate_text(text: str) -> str:
    """Translate a single string using DeepL."""
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'source_lang': SOURCE_LANG,
        'target_lang': TARGET_LANG
    }
    r = requests.get(BASE_URL, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()
    translated = data['translations'][0]['text']
    return translated

def translate_logs(logs: List[SimpleLogMsg], target_lang: str = 'es') -> List[SimpleLogMsg]:
    """Translate the message field of each log entry."""
    translated = []
    for log in logs:
        new_log = log.copy()
        new_log['message'] = translate_text(log['message'])
        translated.append(new_log)
    return translated

if __name__ == '__main__':
    sample = [
        {'message': 'Failed to connect to database', 'timestamp': '2025-08-15T12:00:00Z', 'level': 'ERROR'},
        {'message': 'User session expired', 'timestamp': '2025-08-15T12:05:00Z', 'level': 'WARNING'}
    ]
    translated = translate_logs(sample)
    print(json.dumps(translated, indent=2))
