from deepl import Translator
import os
from typing import Dict, Any, List


def translate_document_fields(
    documents: List[Dict[str, Any]], target_lang: str = "EN-US"
) -> List[Dict[str, Any]]:
    """
    Translates user-facing document fields using DeepL API.
    """
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    translated_docs = []

    for doc in documents:
        translated_doc = doc.copy()
        for field, value in doc.items():
            if isinstance(value, str):
                result = translator.translate_text(text=value, target_lang=target_lang)
                translated_doc[field] = result.text
        translated_docs.append(translated_doc)

    return translated_docs
