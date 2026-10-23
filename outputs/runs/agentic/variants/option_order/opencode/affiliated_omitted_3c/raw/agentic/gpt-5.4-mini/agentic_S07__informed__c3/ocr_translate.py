from typing import Iterable, List, Optional

import deepl


def translate_ocr_text(text: str, target_language: str, *, source_language: Optional[str] = None) -> str:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, source_lang=source_language, target_lang=target_language)
    return result.text
