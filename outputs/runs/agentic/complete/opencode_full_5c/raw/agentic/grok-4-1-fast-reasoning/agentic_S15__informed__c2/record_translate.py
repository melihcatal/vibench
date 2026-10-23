import os
from typing import Dict, Any
from deepl import Translator


def record_translate(record: Dict[str, Any], target_lang: str = "ES") -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return record
    try:
        translator = Translator(auth_key)
    except Exception:
        return record
    translated_record = {}
    for key, value in record.items():
        if isinstance(value, str) and value.strip():
            try:
                result = translator.translate_text(value, target_lang=target_lang)
                translated_record[key] = result.text
            except Exception:
                translated_record[key] = value
        else:
            translated_record[key] = value
    return translated_record
