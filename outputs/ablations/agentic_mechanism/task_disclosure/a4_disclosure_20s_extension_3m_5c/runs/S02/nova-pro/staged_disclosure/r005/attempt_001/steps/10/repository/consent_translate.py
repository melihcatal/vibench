import requests

DEEPL_API_URL = 'https://api.deepl.com/v2/translate'
DEEPL_AUTH_KEY = 'YOUR_DEEPL_AUTH_KEY'

def translate_text(text, target_lang='EN'):
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': target_lang
    }
    response = requests.post(DEEPL_API_URL, data=params)
    response.raise_for_status()
    translations = response.json().get('translations')
    if translations:
        return translations[0]['text']
    return None

if __name__ == '__main__':
    consent_copy = 'Identity provider consent copy to be translated.'
    translated_copy = translate_text(consent_copy)
    if translated_copy:
        print(f'Translated consent copy: {translated_copy}')
    else:
        print('Translation failed.')