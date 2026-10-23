from typing import Optional
from translation_client import get_translator

def translate_markup(markup: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    translator = get_translator()
    result = translator.translate_text(
        markup,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True
    )
    return result.text