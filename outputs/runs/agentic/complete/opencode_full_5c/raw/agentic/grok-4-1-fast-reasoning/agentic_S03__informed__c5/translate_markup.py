from translation_client import get_translator
from translation_models import normalize_input
from typing import Optional


def translate_markup(
    markup: str, source_lang: Optional[str] = None, target_lang: str = "EN-US"
) -> str:
    markup = normalize_input(markup)
    translator = get_translator()
    result = translator.translate_text(
        markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html"
    )
    return result.text
