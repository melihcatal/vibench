"""
Translate user-facing document fields using the OpenAI Chat Completions API with the gpt-4o model.
Uses the official openai Python SDK for OpenAI integration.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_models import DocumentResponse


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL_ID = "gpt-4o"
OPENAI_MODEL_FAMILY = "gpt-4"


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Translate a single text string using OpenAI's gpt-4o model.

    Args:
        text: The text content to translate.
        target_language: Target language name (e.g., "Spanish", "Japanese").
        source_language: Optional source language name. Auto-detected if None.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        Dict with translated text, target language, and model info.
    """
    if client is None:
        api_key = os.environ.get(OPENAI_API_KEY_ENV)
        if not api_key:
            raise EnvironmentError(f"Missing environment variable: {OPENAI_API_KEY_ENV}")
        client = OpenAI(api_key=api_key)

    source_instruction = ""
    if source_language:
        source_instruction = f" from {source_language}"

    prompt = (
        f"Translate the following text{source_instruction} to {target_language}. "
        "Only return the translated text, with no additional commentary.\n\n"
        f"Text: {text}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a professional translation assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    translated = response.choices[0].message.content.strip()

    return {
        "original_text": text,
        "translated_text": translated,
        "target_language": target_language,
        "source_language": source_language or "auto",
        "model_used": OPENAI_MODEL_ID,
        "model_family": OPENAI_MODEL_FAMILY,
    }


def translate_document_fields(
    document: DocumentResponse,
    target_language: str,
    fields_to_translate: Optional[List[str]] = None,
    source_language: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Translate specified string fields of a document using OpenAI gpt-4o.

    Args:
        document: The DocumentResponse whose fields to translate.
        target_language: Target language name.
        fields_to_translate: List of field names to translate.
                             If None, all string-valued top-level fields are translated.
        source_language: Optional source language.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dict with document_id, translated fields, and metadata.
    """
    data = document.data

    if fields_to_translate is None:
        target_fields = [k for k, v in data.items() if isinstance(v, str)]
    else:
        target_fields = [k for k in fields_to_translate if k in data and isinstance(data[k], str)]

    translations: Dict[str, Any] = {}

    for field_name in target_fields:
        text_value = data[field_name]
        if text_value and text_value.strip():
            result = translate_text(
                text=text_value,
                target_language=target_language,
                source_language=source_language,
                client=client,
            )
            translations[field_name] = result["translated_text"]

    return {
        "document_id": document.id,
        "target_language": target_language,
        "translations": translations,
        "model_used": OPENAI_MODEL_ID,
        "model_family": OPENAI_MODEL_FAMILY,
    }


def batch_translate_documents(
    documents: List[DocumentResponse],
    target_language: str,
    fields_to_translate: Optional[List[str]] = None,
    source_language: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Translate fields across multiple documents using OpenAI gpt-4o.

    Args:
        documents: List of DocumentResponse objects.
        target_language: Target language name.
        fields_to_translate: Optional list of field names to translate.
        source_language: Optional source language.
        client: Optional pre-configured OpenAI client.

    Returns:
        List of translation result dicts, one per document.
    """
    results = []
    for doc in documents:
        result = translate_document_fields(
            document=doc,
            target_language=target_language,
            fields_to_translate=fields_to_translate,
            source_language=source_language,
            client=client,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    import json

    sample_doc = DocumentResponse(
        id="doc-001",
        data={
            "title": "Welcome to Our Service",
            "description": "We provide cloud-based document management solutions.",
        },
    )
    result = translate_document_fields(
        sample_doc,
        target_language="Spanish",
        fields_to_translate=["title", "description"],
    )
    print(json.dumps(result, indent=2))
