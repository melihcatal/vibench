import os
from google.cloud import translate_v3 as translate
from database_models import Document, TranslatedDocument
from typing import List, Dict, Any


def translate_document_fields(
    documents: List[Document], fields_to_translate: List[str], target_language: str
) -> List[TranslatedDocument]:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}"
    translated_docs = []

    for doc in documents:
        translated_fields = {}
        for field in fields_to_translate:
            text_to_translate = doc.data.get(field)
            if text_to_translate and isinstance(text_to_translate, str):
                response = client.translate_text(
                    request={
                        "parent": parent,
                        "contents": [text_to_translate],
                        "target_language_code": target_language,
                    }
                )
                translated_fields[field] = response.translations[0].translated_text
            else:
                translated_fields[field] = (
                    text_to_translate  # Keep original if not string or not present
                )

        translated_docs.append(
            TranslatedDocument(
                id=doc.id,
                translated_fields=translated_fields,
                target_language=target_language,
            )
        )
    return translated_docs
