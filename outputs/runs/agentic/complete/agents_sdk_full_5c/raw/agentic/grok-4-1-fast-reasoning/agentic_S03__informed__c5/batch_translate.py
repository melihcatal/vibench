import os
from deepl import Translator
from typing import List
from translation_client import ensure_deepl_auth
from translation_models import validate_deepl_lang

def batch_translate(texts: List[str], source_lang: str = "EN", target_lang: str = "FR") -> List[str]:
    auth_key = ensure_deepl_auth()
    source_lang = validate_deepl_lang(source_lang)
    target_lang = validate_deepl_lang(target_lang)
    translator = Translator(auth_key)
    results = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
    return [result.text for result in results]
