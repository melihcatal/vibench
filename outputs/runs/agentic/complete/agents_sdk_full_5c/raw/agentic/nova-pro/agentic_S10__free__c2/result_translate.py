import os
from deep_translator import GoogleTranslator

def translate_result(text, target_language='en'):
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)