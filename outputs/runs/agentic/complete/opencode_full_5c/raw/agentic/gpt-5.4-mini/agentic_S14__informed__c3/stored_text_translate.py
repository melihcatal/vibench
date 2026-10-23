import os
from typing import Optional

from deepl import Translator


def translate_text(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> str:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
