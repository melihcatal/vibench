import os
from deepl import Translator
from typing import List

def translate_welcome_copy(copy_texts: List[str], target_locale: str) -> List[str]:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = Translator(auth_key)
    results = translator.translate_text(copy_texts, target_lang=target_locale.upper())
    return [result.text for result in results]