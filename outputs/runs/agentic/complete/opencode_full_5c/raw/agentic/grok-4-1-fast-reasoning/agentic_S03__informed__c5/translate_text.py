from translation_client import get_translator
from translation_models import normalize_input
from typing import Optional


def translate_text(
    text: str, source_lang: Optional[str] = None, target_lang: str = "EN-US"
) -> str:
    text = normalize_input(text)
    translator = get_translator()
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
