from typing import Optional
from translation_client import get_translator

def translate_text(text: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    translator = get_translator()
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text