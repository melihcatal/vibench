import os
from deepl import Translator

deepl_auth_key = os.getenv('DEEPL_AUTH_KEY')

translator = Translator(deepl_auth_key)

def translate_transcript(text, target_lang='EN'):
    return translator.translate_text(text, target_lang=target_lang)