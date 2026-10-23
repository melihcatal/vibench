import os
from deepl import Translator
from typing import Dict, Any, List
from translation_client import ensure_deepl_auth
from translation_models import validate_deepl_lang

def translate_dictionary_values(dictionary: Dict[str, str], source_lang: str = "EN", target_lang: str = "FR") -> Dict[str, str]:
    auth_key = ensure_deepl_auth()
    source_lang = validate_deepl_lang(source_lang)
    target_lang = validate_deepl_lang(target_lang)
    translator = Translator(auth_key)
    values: List[str] = list(dictionary.values())
    results = translator.translate_text(values, source_lang=source_lang, target_lang=target_lang)
    translated_values = [result.text for result in results]
    return dict(zip(dictionary.keys(), translated_values))
