"""
[LATER-STEP] record_translate.py
Translate user-facing document fields using DeepL API.
Provider: DeepL API via deepl SDK.
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Dict, Any, List, Optional

import deepl
from database_models import DocumentResponse


def translate_text(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
) -> str:
    """
    Translate a text string using DeepL API.

    Args:
        text: The text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'ES', 'JA', 'ZH').
        source_lang: Optional source language code; if None, DeepL auto-detects.

    Returns:
        The translated text string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    return result.text


def translate_document_fields(
    document: DocumentResponse,
    target_lang: str = "EN",
    fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Translate specified user-facing fields of a document into the target language.

    Args:
        document: The DocumentResponse to translate.
        target_lang: Target language code for DeepL (e.g., 'EN', 'DE', 'FR').
        fields: Optional list of data field names to translate
                (default: ['body', 'title', 'content', 'description']).

    Returns:
        A dictionary mapping field names to their translated text.
    """
    if fields is None:
        fields = ["body", "title", "content", "description"]

    translations = {}
    for field_name in fields:
        field_value = document.data.get(field_name)
        if field_value and isinstance(field_value, str):
            translated = translate_text(field_value, target_lang=target_lang)
            translations[field_name] = translated

    return translations


def translate_all_documents(
    documents: List[DocumentResponse],
    target_lang: str = "EN",
    fields: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Translate fields across a list of documents.

    Args:
        documents: List of DocumentResponse objects.
        target_lang: Target language code.
        fields: Optional list of fields to translate.

    Returns:
        List of translation result dicts, one per document.
    """
    all_results = []
    for doc in documents:
        result = {"document_id": doc.document_id}
        translations = translate_document_fields(doc, target_lang=target_lang, fields=fields)
        result["translations"] = translations
        all_results.append(result)
    return all_results


if __name__ == "__main__":
    sample = DocumentResponse(
        document_id="doc-001",
        data={"title": "Bonjour le monde", "body": "Ceci est un texte en français."},
    )
    translated = translate_document_fields(sample, target_lang="EN")
    print(translated)
