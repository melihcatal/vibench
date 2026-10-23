from typing import Optional
import deepl
from translation_client import get_translator

def translate_markup(markup: str, source_lang: str = "auto", target_lang: str) -> str:
    """
    Translates HTML or markup while preserving tags using DeepL.
    """
    translator = get_translator()
    sl = None if source_lang.lower() == "auto" else source_lang
    result = translator.translate_text(
        markup, 
        target_lang=target_lang, 
        source_lang=sl, 
        tag_handling="html"
    )
    return result.text
