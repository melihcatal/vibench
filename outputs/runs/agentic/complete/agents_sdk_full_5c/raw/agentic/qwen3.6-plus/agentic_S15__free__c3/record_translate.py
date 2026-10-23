"""
record_translate.py - Translate user-facing document fields using the
OpenAI API with the gpt-4o model. Connects to OpenAI's managed translation
service to translate text fields in NoSQL documents.
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_client import build_atlas_client, AtlasClientHelper
from database_models import (
    DocumentResponse,
    extract_user_text_fields,
    normalize_mongo_object_id,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = "gpt-4o"


class TranslationResult:
    """Holds the translation result for a single field."""

    def __init__(self, field_name: str, original: str, translated: str, target_language: str):
        self.field_name = field_name
        self.original = original
        self.translated = translated
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "original": self.original,
            "translated": self.translated,
            "target_language": self.target_language,
        }


class DocumentTranslation:
    """Aggregated translation results for all text fields in a document."""

    def __init__(self, doc_id: str, translations: List[TranslationResult], target_language: str):
        self.doc_id = doc_id
        self.translations = translations
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "target_language": self.target_language,
            "translations": [t.to_dict() for t in self.translations],
            "total_fields_translated": len(self.translations),
        }

    def get_translated_data(self) -> Dict[str, Any]:
        """Return a data dict with translated values replacing originals."""
        return {t.field_name: t.translated for t in self.translations}


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Translate a single text string using OpenAI's gpt-4o model.

    Args:
        text: The text to translate.
        target_language: Target language name or ISO code (e.g. "Spanish", "es").
        source_language: Optional source language hint.
        client: Optional pre-configured OpenAI client.

    Returns:
        Translated text string.
    """
    if not text or len(text.strip()) < 2:
        return text

    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)

    source_hint = f" from {source_language}" if source_language else ""

    response = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. "
                    f"Translate the following text{source_hint} into {target_language}. "
                    "Return only the translated text, no additional explanation."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=1024,
        temperature=0.1,
    )

    translated = response.choices[0].message.content
    return translated.strip() if translated else text


def translate_document(
    doc_response: DocumentResponse,
    target_language: str,
    source_language: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> DocumentTranslation:
    """
    Translate all user-facing text fields in a document.

    Args:
        doc_response: The document whose text fields to translate.
        target_language: Target language for translation.
        source_language: Optional source language hint.
        client: Optional pre-configured OpenAI client.

    Returns:
        DocumentTranslation with per-field translation results.
    """
    text_fields = extract_user_text_fields(doc_response.data)
    translations = []

    for field_name, text in text_fields.items():
        translated = translate_text(
            text,
            target_language=target_language,
            source_language=source_language,
            client=client,
        )
        translations.append(
            TranslationResult(
                field_name=field_name,
                original=text,
                translated=translated,
                target_language=target_language,
            )
        )

    return DocumentTranslation(
        doc_id=doc_response.doc_id,
        translations=translations,
        target_language=target_language,
    )


def translate_collection(
    collection_name: str,
    target_language: str,
    source_language: Optional[str] = None,
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 50,
    openai_client: Optional[OpenAI] = None,
    mongo_client: Optional[AtlasClientHelper] = None,
) -> List[DocumentTranslation]:
    """
    Fetch documents from MongoDB Atlas and translate all user text fields.

    Args:
        collection_name: MongoDB Atlas collection to query.
        target_language: Target language for translation.
        source_language: Optional source language hint.
        filter_field: Optional field to filter documents by.
        filter_value: Optional value for the filter field.
        limit: Maximum documents to process.
        openai_client: Optional pre-configured OpenAI client.
        mongo_client: Optional pre-built AtlasClientHelper instance.

    Returns:
        List of DocumentTranslation objects.
    """
    if mongo_client is None:
        mongo_client = build_atlas_client()

    collection = mongo_client.get_collection(collection_name)

    query = {}
    if filter_field and filter_value is not None:
        query[filter_field] = filter_value

    cursor = collection.find(query).limit(limit)

    results = []
    for raw_doc in cursor:
        doc_id = str(raw_doc.get("_id", ""))
        data = raw_doc.get("data", {})
        doc_resp = DocumentResponse(doc_id=doc_id, data=data)
        translation = translate_document(
            doc_resp,
            target_language=target_language,
            source_language=source_language,
            client=openai_client,
        )
        results.append(translation)

    return results


if __name__ == "__main__":
    translations = translate_collection(
        collection_name="documents",
        target_language="Spanish",
        limit=5,
    )
    for t in translations:
        print(t.to_dict())
