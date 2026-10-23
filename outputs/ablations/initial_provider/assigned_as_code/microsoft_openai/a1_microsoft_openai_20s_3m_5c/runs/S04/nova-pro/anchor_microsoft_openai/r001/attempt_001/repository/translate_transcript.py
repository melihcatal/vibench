import os
import requests


def translate_transcript(text, target_language='en'):
    response = requests.post(
        'https://api.deepl.com/v2/translate',
        params={'auth_key': os.environ['DEEPL_API_KEY'], 'text': text, 'target_lang': target_language},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['translations'][0]['text']