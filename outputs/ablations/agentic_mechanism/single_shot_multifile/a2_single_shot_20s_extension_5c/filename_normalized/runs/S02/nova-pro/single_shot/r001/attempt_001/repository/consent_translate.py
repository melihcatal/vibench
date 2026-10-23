import os
from deep_translator import GoogleTranslator

def translate_consent(text, target_lang='es'):
    translator = GoogleTranslator(source='auto', target=target_lang)
    translated_text = translator.translate(text)
    return translated_text
