import os
from typing import Optional
from deepl import Translator

def translate_script(script: str, target_lang: str = 'EN-US') -> str:
    """
    Translates narration script to target language using DeepL API.
    """
    api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        raise ValueError('DEEPL_API_KEY environment variable not set')
    translator = Translator(api_key)
    result = translator.translate_text(script, target_lang=target_lang)
    return result.text
