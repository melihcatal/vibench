import os
import deepl
from typing import Optional

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise ValueError("DEEPL_AUTH_KEY must be set.")

translator = deepl.Translator(DEEPL_AUTH_KEY)

def translate_result(text: str, target_lang: str = "FR") -> str:
    """Translate text to target language using DeepL."""
    result = translator.translate_text(text, target_lang=deepl.TargetLanguage(target_lang))
    return result.text