from typing import Dict, List, Any
from google.cloud import translate_v2 as translate


def record_translate(
    documents: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    client = translate.Client()

    translated_documents = []
    for document in documents:
        document_data = document.get("document_data", {})
        translated_data = {}

        for key, value in document_data.items():
            if isinstance(value, str):
                translated_data[key] = client.translate(
                    value, target_language=target_language
                )["translatedText"]
            else:
                translated_data[key] = value

        translated_documents.append(
            {"document_id": document.get("id"), "translated_data": translated_data}
        )

    return translated_documents
