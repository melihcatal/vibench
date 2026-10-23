from translation_client import get_deepl_translator
from typing import Optional


def translate_text(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> str:
    translator = get_deepl_translator()
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    if isinstance(result, list):
        return result[0].text
    return result.text
