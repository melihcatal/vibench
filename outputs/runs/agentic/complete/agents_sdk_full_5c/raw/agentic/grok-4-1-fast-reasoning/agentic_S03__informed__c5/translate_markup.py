import os
from deepl import Translator
from translation_client import ensure_deepl_auth
from translation_models import validate_deepl_lang

def translate_markup(markup: str, source_lang: str = "EN", target_lang: str = "FR") -> str:
    auth_key = ensure_deepl_auth()
    source_lang = validate_deepl_lang(source_lang)
    target_lang = validate_deepl_lang(target_lang)
    translator = Translator(auth_key)
    result = translator.translate_text(markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html")
    return result.text
