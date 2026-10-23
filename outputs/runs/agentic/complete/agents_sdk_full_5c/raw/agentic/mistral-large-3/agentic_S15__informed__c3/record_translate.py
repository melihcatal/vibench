from typing import Dict, Any
import deepl
import os

def translate_text(text: str, target_lang: str) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

def translate_document_fields(document: Dict[str, Any], fields: list[str], target_lang: str) -> Dict[str, Any]:
    translated = document.copy()
    for field in fields:
        if field in document:
            translated[field] = translate_text(str(document[field]), target_lang)
    return translated