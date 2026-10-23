import os
from typing import Optional
from deepl import Translator

def translate_markup(markup: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html")
    return result.text