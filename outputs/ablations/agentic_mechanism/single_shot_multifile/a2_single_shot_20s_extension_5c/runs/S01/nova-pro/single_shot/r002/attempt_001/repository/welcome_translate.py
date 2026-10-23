import os
from deepl import Translator

def translate_welcome(text, target_lang):
    api_key = os.getenv('DEEPL_API_KEY')
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text