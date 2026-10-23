import os
import deepl
from typing import Dict, Any

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_record_fields(
    record: Dict[str, Any], target_lang: str = "EN"
) -> Dict[str, Any]:
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            result = translator.translate_text(value, target_lang=target_lang)
            translated[key] = result.text
        else:
            translated[key] = value
    return translated
