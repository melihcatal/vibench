import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

def translate_consent(text):
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang='ES')
    print(result.text)