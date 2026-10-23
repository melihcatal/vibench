import deepl
import os
from typing import Optional

def translate_markup(markup: str, source_lang: Optional[str] = "auto", target_lang: str) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html")
    return result.text
