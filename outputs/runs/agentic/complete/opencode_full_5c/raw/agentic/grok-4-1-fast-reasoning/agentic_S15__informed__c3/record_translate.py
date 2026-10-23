import os
import deepl
from typing import Dict, Any


def translate_record(record: Dict[str, Any], target_lang: str = "EN") -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    translated_data = record["data"].copy()
    for key, value in record["data"].items():
        if isinstance(value, str) and value.strip():
            try:
                translation = translator.translate_text(value, target_lang=target_lang)
                translated_data[key] = translation.text
            except Exception:
                pass
    return {"id": record["id"], "data": translated_data, "version": record["version"]}
