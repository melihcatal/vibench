import os
from typing import Dict
import deepl

# DeepL API
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

def translate_consent_copy(consent_text: str, target_lang: str) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(consent_text, target_lang=target_lang)
    return result.text