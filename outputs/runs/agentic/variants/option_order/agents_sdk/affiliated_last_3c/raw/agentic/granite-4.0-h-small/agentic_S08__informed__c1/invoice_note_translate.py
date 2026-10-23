import json
from typing import List
from deep_translator import GoogleTranslator

def translate_notes(text: str, target_lang: str = 'en') -> str:
    translator = GoogleTranslator(source='auto', target=target_lang)
    try:
        translated = translator.translate(text)
    except Exception as e:
        # Fallback to original text on error
        return text
    return translated
