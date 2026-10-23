from typing import Optional
from deepl import Translator
from translation_client import load_deepl_api_key
from translation_models import normalize_language_code

def translate_markup(markup: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    api_key = load_deepl_api_key()
    translator = Translator(api_key)
    source_lang = normalize_language_code(source_lang)
    result = translator.translate_text(
        markup,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="html"
    )
    return result.text
