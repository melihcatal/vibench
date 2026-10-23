import os
import deepl

def translate_record(record: dict, target_lang: str = 'EN') -> dict:
    auth_key = os.environ.get('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError('DEEPL_AUTH_KEY environment variable is required.')
    translator = deepl.Translator(auth_key)
    translated = {}
    for key, value in record.items():
        if isinstance(value, str) and value.strip():
            result = translator.translate_text(value, target_lang=target_lang)
            translated[key] = result.text
        else:
            translated[key] = value
    return translated