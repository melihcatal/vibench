import os
import deepl

def ocr_translate(text: str, target_lang: str = 'FR') -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
