import os
import deepl
from database_models import Document


def translate_record(record: Document, target_lang: str = "EN") -> Document:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated = record.copy()
    text_fields = ["title", "description", "content"]
    for field in text_fields:
        if field in record and isinstance(record[field], str) and record[field].strip():
            try:
                result = translator.translate_text(
                    record[field], target_lang=target_lang
                )
                translated[field] = result.text
            except Exception:
                pass
    return translated
