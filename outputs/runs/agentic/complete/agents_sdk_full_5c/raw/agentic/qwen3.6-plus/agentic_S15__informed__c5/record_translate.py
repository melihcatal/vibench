"""
Translate user-facing document fields using Azure AI Translator.

Uses the azure-ai-translation-text SDK to call the Microsoft Translator
REST API for translating document content between languages.
Requires AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables.
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import RequestException

from database_models import extract_text_fields


AZURE_TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com",
)


def translate_document_fields(
    document: Dict[str, Any],
    target_language: str = "es",
    source_language: Optional[str] = None,
    text_fields: Optional[List[str]] = None,
    include_original: bool = True,
) -> Dict[str, Any]:
    """Translate user-facing text fields in a document using Azure AI Translator.

    Args:
        document: The document dict containing text fields to translate.
        target_language: ISO 639-1 language code for translation target (default: 'es').
        source_language: Optional ISO 639-1 source language code. If None, auto-detect.
        text_fields: Specific field names to translate. If None, common text fields
                     (title, description, content, body, text, summary, notes) are used.
        include_original: Whether to include original text alongside translations.

    Returns:
        Dict with 'success', 'translated_document', and optional 'error'.
    """
    api_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not api_key or not region:
        return {
            "success": False,
            "error": (
                "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION "
                "environment variables are required"
            ),
            "translated_document": None,
        }

    texts = extract_text_fields(document, text_fields)
    fields_to_translate = text_fields or [
        "title", "description", "content", "body", "text", "summary", "notes"
    ]

    if not texts:
        return {
            "success": True,
            "translated_document": document,
            "message": "No translatable text fields found in document",
        }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    params = {
        "api-version": "3.0",
        "to": target_language,
    }

    if source_language:
        params["from"] = source_language

    body = [{"text": text} for text in texts]

    try:
        url = f"{AZURE_TRANSLATOR_ENDPOINT}/translate"
        response = requests.post(url, headers=headers, params=params, json=body)
        response.raise_for_status()

        translations = response.json()
        translated_document = dict(document)
        field_translations = {}

        for idx, translation in enumerate(translations):
            if idx < len(fields_to_translate):
                field_name = fields_to_translate[idx]
                translated_text = translation["translations"][0]["text"]
                detected = translation.get("detectedLanguage", {})

                field_translations[field_name] = {
                    "original": document.get(field_name, ""),
                    "translated": translated_text,
                    "detected_language": detected.get("language"),
                    "confidence": detected.get("score"),
                    "target_language": target_language,
                }

                translated_document[f"{field_name}_{target_language}"] = translated_text

                if not include_original and field_name in translated_document:
                    # Keep original but mark as translated
                    pass

        return {
            "success": True,
            "translated_document": translated_document,
            "field_translations": field_translations,
            "target_language": target_language,
            "source_language": source_language or "auto-detected",
        }

    except RequestException as exc:
        return {
            "success": False,
            "error": str(exc),
            "translated_document": None,
        }


def translate_multiple_documents(
    documents: List[Dict[str, Any]],
    target_language: str = "es",
    source_language: Optional[str] = None,
    text_fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Translate multiple documents and return aggregated results."""
    all_translated = []
    all_field_translations = {}

    for doc in documents:
        result = translate_document_fields(
            document=doc,
            target_language=target_language,
            source_language=source_language,
            text_fields=text_fields,
        )
        if result.get("success"):
            all_translated.append(result.get("translated_document"))
            if result.get("field_translations"):
                doc_id = doc.get("doc_id", doc.get("document_id", "unknown"))
                all_field_translations[doc_id] = result["field_translations"]

    return {
        "success": True,
        "translated_documents": all_translated,
        "field_translations": all_field_translations,
        "target_language": target_language,
        "document_count": len(all_translated),
    }


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        data = json.loads(raw_input)
    else:
        data = {
            "document": {
                "doc_id": "doc-001",
                "title": "Welcome to Our Platform",
                "content": "Thank you for joining us. We are excited to have you on board.",
            },
            "target_language": "es",
            "source_language": "en",
        }

    if "documents" in data:
        result = translate_multiple_documents(
            documents=data["documents"],
            target_language=data.get("target_language", "es"),
            source_language=data.get("source_language"),
            text_fields=data.get("text_fields"),
        )
    else:
        result = translate_document_fields(
            document=data.get("document", {}),
            target_language=data.get("target_language", "es"),
            source_language=data.get("source_language"),
            text_fields=data.get("text_fields"),
        )
    print(json.dumps(result, indent=2))
