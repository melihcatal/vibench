import os
from deep_translator import GoogleTranslator

def appeal_translate(text, target_lang='en'):
    translator = GoogleTranslator(source='auto', target=target_lang)
    return translator.translate(text)