import json
import googletrans
from database_models import DatabaseModels

# Google Translate API (managed provider) used for demo


def record_translate(record: dict, target_lang: str = "es") -> dict:
    """Translate user-facing fields in a document to the target language.

    Uses googletrans (a wrapper around Google Translate) as the concrete provider.","""
    translator = googletrans.Translator()
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            translated[key] = translator.translate(value, dest=target_lang).text
        else:
            translated[key] = value
    return translated
