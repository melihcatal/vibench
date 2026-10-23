import os
from deep_translator import GoogleTranslator

def translate_consent(text, target_language='es'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_text = translator.translate(text)
    return translated_text