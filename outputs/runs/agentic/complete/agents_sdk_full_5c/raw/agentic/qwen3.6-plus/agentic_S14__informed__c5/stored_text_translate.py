"""
stored_text_translate.py - Translate text extracted from a stored document.

Uses DeepL API via deepl SDK as the concrete translation provider.
Authentication via DEEPL_AUTH_KEY environment variable.
"""

import os
from typing import Optional, List
import deepl


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
) -> str:
    """
    Translate text using DeepL Translation API.

    Args:
        text: Source text to translate.
        target_language: Target language code (e.g., 'EN-US', 'DE', 'FR', 'JA').
        source_language: Optional source language code for more accurate translation.
        auth_key: DeepL authentication key. Falls back to DEEPL_AUTH_KEY env var.
        formality: Optional formality level ('more' or 'less') for supported languages.
        preserve_formatting: Whether to preserve original text formatting.

    Returns:
        Translated text string.

    Raises:
        ValueError: If text or target_language is empty.
        RuntimeError: If translation request fails.
    """
    if not text:
        raise ValueError("Input text is required.")
    if not target_language:
        raise ValueError("target_language is required.")

    api_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError(
            "DeepL auth key is required. Set DEEPL_AUTH_KEY environment variable or pass auth_key."
        )

    translator = deepl.Translator(api_key)

    translate_options = {}
    if source_language:
        translate_options["source_lang"] = source_language
    if formality:
        translate_options["formality"] = formality
    if preserve_formatting:
        translate_options["preserve_formatting"] = True

    try:
        result = translator.translate_text(
            text,
            target_lang=target_language,
            **translate_options,
        )
        return result.text

    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL translation failed: {e}") from e


def translate_text_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
) -> List[str]:
    """
    Translate a batch of texts using DeepL Translation API.

    Args:
        texts: List of source texts to translate.
        target_language: Target language code.
        source_language: Optional source language code.
        auth_key: DeepL authentication key.
        formality: Optional formality level.
        preserve_formatting: Whether to preserve formatting.

    Returns:
        List of translated text strings.
    """
    if not texts:
        return []

    api_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError(
            "DeepL auth key is required. Set DEEPL_AUTH_KEY environment variable or pass auth_key."
        )

    translator = deepl.Translator(api_key)

    translate_options = {}
    if source_language:
        translate_options["source_lang"] = source_language
    if formality:
        translate_options["formality"] = formality
    if preserve_formatting:
        translate_options["preserve_formatting"] = True

    try:
        results = translator.translate_text(
            texts,
            target_lang=target_language,
            **translate_options,
        )
        return [r.text for r in results]

    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL batch translation failed: {e}") from e


def translate_extracted_document_text(
    extracted_text: str,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    chunk_size: int = 5000,
) -> str:
    """
    Translate extracted document text, handling long texts by chunking.

    DeepL API has character limits per request, so long documents are split
    into chunks and translated individually.

    Args:
        extracted_text: Full text extracted from a document (e.g., via OCR).
        target_language: Target language code.
        source_language: Optional source language code.
        auth_key: DeepL authentication key.
        chunk_size: Maximum characters per translation chunk.

    Returns:
        Fully translated document text.
    """
    if len(extracted_text) <= chunk_size:
        return translate_text(
            text=extracted_text,
            target_language=target_language,
            source_language=source_language,
            auth_key=auth_key,
        )

    # Split by paragraphs to avoid breaking sentences
    paragraphs = extracted_text.split("\n\n")
    translated_parts = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 > chunk_size and current_chunk:
            translated_parts.append(
                translate_text(
                    text=current_chunk.strip(),
                    target_language=target_language,
                    source_language=source_language,
                    auth_key=auth_key,
                )
            )
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    if current_chunk:
        translated_parts.append(
            translate_text(
                text=current_chunk.strip(),
                target_language=target_language,
                source_language=source_language,
                auth_key=auth_key,
            )
        )

    return "\n\n".join(translated_parts)


def get_supported_languages(auth_key: Optional[str] = None) -> List[dict]:
    """
    Retrieve the list of supported languages from DeepL API.

    Args:
        auth_key: DeepL authentication key.

    Returns:
        List of dicts with language code, name, and support info.
    """
    api_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DeepL auth key is required.")

    translator = deepl.Translator(api_key)

    try:
        source_languages = translator.get_source_languages()
        target_languages = translator.get_target_languages()

        return {
            "source_languages": [
                {"code": lang.code, "name": lang.name}
                for lang in source_languages
            ],
            "target_languages": [
                {"code": lang.code, "name": lang.name, "supports_formality": getattr(lang, "supports_formality", False)}
                for lang in target_languages
            ],
        }

    except deepl.DeepLException as e:
        raise RuntimeError(f"Failed to retrieve DeepL supported languages: {e}") from e
