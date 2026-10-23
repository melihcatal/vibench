# record_translate.py
"""
Later-step integration file for translating user-facing fields of a document.
Uses a managed translation service (e.g., DeepL, Google Cloud Translation) via its SDK.
"""

import os
from google.cloud import translate_v2 as translate
from database_models import Document


def translate_document(doc: Document, target_lang: str = "es") -> Document:
    """Translate all string fields in a document's 'content' to the target language.

    Args:
        doc (Document): Document to translate.
        target_lang (str): ISO language code (default 'es' for Spanish).

    Returns:
        Document: New Document instance with translated content.
    """
    # Environment variable for auth; defaults to application-default credentials
    client = translate.Client()
    translated = {}
    for key, value in doc.content.items():
        if isinstance(value, str):
            # Translate text
            result = client.translate(value, target_language=target_lang)
            translated[key] = result["translatedText"]
        else:
            translated[key] = value  # non-string fields unchanged
    # Build and return a new Document preserving other fields
    new_data = {
        "id": doc.id,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
        "content": translated,
        "version": doc.version,
    }
    return Document(**new_data)
