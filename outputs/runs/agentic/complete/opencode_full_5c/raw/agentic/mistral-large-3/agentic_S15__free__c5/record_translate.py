from typing import Dict, List
from deep_translator import GoogleTranslator


def record_translate(
    documents: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Translate user-facing document fields using Google Translate."""
    translated_docs = []

    for doc in documents:
        translated_fields = {}
        for field, value in doc["body"].items():
            if isinstance(value, str):
                translated_fields[field] = GoogleTranslator(
                    source="auto", target=target_language
                ).translate(value)

        translated_docs.append(
            {
                "document_id": doc["id"],
                "original_language": "auto",
                "translated_language": target_language,
                "translated_fields": translated_fields,
            }
        )

    return translated_docs
