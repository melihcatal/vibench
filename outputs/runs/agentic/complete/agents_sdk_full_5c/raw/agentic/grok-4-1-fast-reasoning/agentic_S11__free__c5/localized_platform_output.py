import requests
import os

def translate_platform_output_to_locale(
    output_text: str,
    target_lang: str = 'FR'
) -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    url = 'https://api-free.deepl.com/v2/translate'
    data = {
        'auth_key': auth_key,
        'text': output_text,
        'target_lang': target_lang
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    translations = response.json()['translations']
    return translations[0]['text']