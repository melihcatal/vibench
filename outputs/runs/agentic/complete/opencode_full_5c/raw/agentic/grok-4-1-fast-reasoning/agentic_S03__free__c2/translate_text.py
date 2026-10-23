from typing import Optional
import deepl
from translation_client import get_translator

def translate_text(text: str, source_lang: str = "auto", target_lang: str) -> str:
    """
    Translates a single text string between languages using DeepL.
    """
    translator = get_translator()
    sl = None if source_lang.lower() == "auto" else source_lang
    result = translator.translate_text(text, target_lang=target_lang, source_lang=sl)
    return result.text
