import os
from deepl import Translator

translator = Translator(os.getenv('DEEPL_AUTH_KEY'))

def translate_record(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)