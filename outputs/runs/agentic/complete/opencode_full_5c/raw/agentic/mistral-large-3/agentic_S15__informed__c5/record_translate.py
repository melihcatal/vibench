from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any, List


def translate_document_fields(
    documents: List[Dict[str, Any]], target_language: str, fields: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Translates user-facing document fields using Google Cloud Translation.

    Args:
        documents: List of documents to translate
        target_language: Target language code (e.g., 'es', 'fr')
        fields: List of field names to translate (None for all string fields)

    Returns:
        List of documents with translated fields
    """
    client = translate.Client()

    if not client:
        raise ValueError(
            "Google Cloud credentials must be set via GOOGLE_APPLICATION_CREDENTIALS"
        )

    translated_docs = []
    for doc in documents:
        translated_doc = doc.copy()

        for key, value in doc.items():
            if fields and key not in fields:
                continue
            if isinstance(value, str):
                result = client.translate(value, target_language=target_language)
                translated_doc[key] = result["translatedText"]
            elif isinstance(value, list):
                translated_doc[key] = [
                    client.translate(item, target_language=target_language)[
                        "translatedText"
                    ]
                    if isinstance(item, str)
                    else item
                    for item in value
                ]

        translated_docs.append(translated_doc)

    return translated_docs
