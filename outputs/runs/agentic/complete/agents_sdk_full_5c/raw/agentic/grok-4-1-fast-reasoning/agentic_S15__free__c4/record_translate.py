import os
from typing import Dict, Any
import deepl

auth_key = os.getenv("DEEPL_AUTH_KEY")
if not auth_key:
    raise ValueError("DEEPL_AUTH_KEY environment variable required")

translator = deepl.Translator(auth_key)

def translate_document_fields(doc: Dict[str, Any], target_lang: str = "EN-US") -> Dict[str, Any]:
    translated_doc = {}
    for key, value in doc.items():
        if isinstance(value, str) and value.strip():
            translation = translator.translate_text(value, target_lang=target_lang)
            translated_doc[key] = translation.text
        else:
            translated_doc[key] = value
    return translated_doc