"""
Translate text extracted from a stored document using the DeepL API.

Uses the DeepL translation service (deepl Python SDK) to translate
extracted text between languages. Authentication via DEEPL_AUTH_KEY
environment variable.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import deepl

logger = logging.getLogger(__name__)

# Provider-identifying environment variable for DeepL API
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_API_URL = "https://api.deepl.com"
DEEPL_API_URL_FREE = "https://api-free.deepl.com"

# Common language codes supported by DeepL
DEEPL_LANGUAGES = {
    "EN": "English",
    "DE": "German",
    "FR": "French",
    "ES": "Spanish",
    "IT": "Italian",
    "PT": "Portuguese",
    "NL": "Dutch",
    "PL": "Polish",
    "RU": "Russian",
    "JA": "Japanese",
    "ZH": "Chinese",
    "KO": "Korean",
    "AR": "Arabic",
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "EL": "Greek",
    "FI": "Finnish",
    "HU": "Hungarian",
    "ID": "Indonesian",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NB": "Norwegian (Bokmål)",
    "RO": "Romanian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "TR": "Turkish",
    "UK": "Ukrainian",
}


def create_deepl_translator(
    auth_key: Optional[str] = None,
    server_url: Optional[str] = None,
) -> deepl.Translator:
    """
    Create a DeepL Translator client.

    Args:
        auth_key: DeepL API key. Falls back to DEEPL_AUTH_KEY env var.
        server_url: API endpoint. Defaults to api.deepl.com or api-free.deepl.com.

    Returns:
        Configured deepl.Translator instance.
    """
    key = auth_key or os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not key:
        raise ValueError(
            f"DeepL API key not provided. Set the {DEEPL_AUTH_KEY_ENV} environment variable."
        )

    if server_url is None:
        # Use free API URL if key indicates a free plan
        if key.endswith(":fx"):
            server_url = DEEPL_API_URL_FREE
        else:
            server_url = DEEPL_API_URL

    translator = deepl.Translator(
        auth_key=key,
        server_url=server_url,
    )
    logger.debug("Created DeepL translator for endpoint %s", server_url)
    return translator


def translate_text(
    text: str,
    target_lang: str,
    *,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
    split_sentences: str = "on",
) -> str:
    """
    Translate text using the DeepL API.

    Args:
        text: Source text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code. If None, DeepL auto-detects.
        auth_key: Optional DeepL API key.
        translator: Optional pre-created deepl.Translator instance.
        formality: 'more' or 'less' for supported languages.
        preserve_formatting: Whether to preserve formatting tags.
        split_sentences: 'on', 'off', or 'nonewlines'.

    Returns:
        Translated text string.
    """
    if translator is None:
        translator = create_deepl_translator(auth_key=auth_key)

    target_lang_upper = target_lang.upper()
    source_lang_upper = source_lang.upper() if source_lang else None

    translate_kwargs: dict = {
        "target_lang": target_lang_upper,
        "preserve_formatting": preserve_formatting,
        "split_sentences": split_sentences,
    }
    if source_lang_upper:
        translate_kwargs["source_lang"] = source_lang_upper
    if formality:
        translate_kwargs["formality"] = formality

    try:
        result = translator.translate_text(text, **translate_kwargs)
    except deepl.DeepLException as exc:
        logger.error("DeepL translation failed: %s", exc)
        raise

    translated = result.text
    logger.info(
        "DeepL translated text from '%s' to '%s' (%d -> %d chars)",
        source_lang or "auto-detect",
        target_lang_upper,
        len(text),
        len(translated),
    )
    return translated


def translate_chunks(
    texts: list[str],
    target_lang: str,
    *,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> list[str]:
    """
    Translate multiple text chunks using the DeepL API.

    Uses DeepL's batch translation for efficiency when translating
    multiple segments at once.

    Args:
        texts: List of source text strings.
        target_lang: Target language code.
        source_lang: Source language code (optional, auto-detect if None).
        auth_key: Optional DeepL API key.
        translator: Optional pre-created deepl.Translator.

    Returns:
        List of translated text strings in the same order as input.
    """
    if translator is None:
        translator = create_deepl_translator(auth_key=auth_key)

    if not texts:
        return []

    translate_kwargs: dict = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    try:
        results = translator.translate_text(texts, **translate_kwargs)
    except deepl.DeepLException as exc:
        logger.error("DeepL batch translation failed: %s", exc)
        raise

    # Handle both single TextResult and list of TextResult
    if isinstance(results, list):
        return [r.text for r in results]
    else:
        return [results.text]


def translate_document_text(
    extracted_text: str,
    target_lang: str,
    *,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
    chunk_size: int = 5000,
) -> str:
    """
    Translate document text by splitting into chunks for the DeepL API.

    The DeepL API has a request size limit, so long documents are
    split into chunks, translated individually, and recombined.

    Args:
        extracted_text: Full document text to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional).
        auth_key: Optional DeepL API key.
        translator: Optional pre-created deepl.Translator.
        chunk_size: Maximum characters per translation chunk.

    Returns:
        Full translated document text.
    """
    if len(extracted_text) <= chunk_size:
        return translate_text(
            extracted_text,
            target_lang,
            source_lang=source_lang,
            auth_key=auth_key,
            translator=translator,
        )

    # Split on paragraph boundaries where possible
    paragraphs = extracted_text.split("\n\n")
    chunks: list[str] = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    translated_chunks = translate_chunks(
        chunks,
        target_lang,
        source_lang=source_lang,
        auth_key=auth_key,
        translator=translator,
    )

    return "\n\n".join(translated_chunks)
