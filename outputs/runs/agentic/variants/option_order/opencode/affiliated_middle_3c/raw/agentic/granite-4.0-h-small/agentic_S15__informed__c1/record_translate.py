# LATER-STEP
# record_translate.py - Translate user-facing document fields

# Provider: Google Cloud Translation (general text translation)
from google.cloud import translate_v2 as translate
import json
from database_models import DocumentResponse

translate_client = translate.Client()


def translate_record(record: dict, target_lang: str = "es") -> dict:
    """Translate all string values in a document record to a target language.

    Args:
        record (dict): Source language document fields.
        target_lang (str): ISO language code to translate into.

    Returns:
        dict: New record with translated text.
    """
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            translated[key] = translate_client.translate(
                value, target_language=target_lang
            )["translatedText"]
        else:
            translated[key] = value  # non-string values copied unchanged
    return translated
