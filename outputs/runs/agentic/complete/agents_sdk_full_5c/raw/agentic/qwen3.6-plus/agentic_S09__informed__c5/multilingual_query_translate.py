"""
[LATER-STEP] Translate queries before multilingual embedding search.
Provider: DeepL API
SDK: requests (REST) with direct API calls
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional, Dict

import requests


DEEPL_API_HOST = "api.deepl.com"
DEEPL_API_URL = f"https://{DEEPL_API_HOST}/v2/translate"


@dataclass
class TranslationResult:
    """Single translation result from DeepL."""
    original_text: str
    translated_text: str
    source_lang: str = ""
    target_lang: str = "en"


@dataclass
class BatchTranslationResult:
    """Aggregated translation results."""
    translations: List[TranslationResult] = []
    total_characters: int = 0


def translate_query(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    """
    Translate a single query string using the DeepL API before embedding search.

    DeepL supports high-quality machine translation across many languages,
    enabling multilingual semantic search by translating queries to a common
    language before embedding.

    Args:
        text: The query text to translate.
        target_lang: Target language code (e.g., "EN", "DE", "FR", "ES", "JA").
        source_lang: Source language code (optional; DeepL auto-detects if None).
        api_key: DeepL API key (falls back to DEEPL_AUTH_KEY env var).
        formality: Formality preference ("more", "less", or None).

    Returns:
        TranslationResult with original and translated text.
    """
    key = api_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL translation.")

    data: Dict = {
        "text": [text],
        "target_lang": target_lang.upper(),
        "auth_key": key,
    }

    if source_lang:
        data["source_lang"] = source_lang.upper()

    if formality in ("more", "less"):
        data["formality"] = formality

    response = requests.post(DEEPL_API_URL, data=data)
    response.raise_for_status()

    result_data = response.json()
    translations = result_data.get("translations", [])

    if not translations:
        return TranslationResult(
            original_text=text,
            translated_text=text,
            target_lang=target_lang,
        )

    first = translations[0]
    detected_source = first.get("detected_source_language", source_lang or "")

    return TranslationResult(
        original_text=text,
        translated_text=first.get("text", text),
        source_lang=detected_source,
        target_lang=target_lang,
    )


def translate_queries_batch(
    texts: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
) -> BatchTranslationResult:
    """
    Translate multiple queries in a single DeepL API call.

    Args:
        texts: List of query strings to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional; auto-detected if None).
        api_key: DeepL API key (falls back to DEEPL_AUTH_KEY env var).

    Returns:
        BatchTranslationResult with all translations.
    """
    key = api_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL translation.")

    data: Dict = {
        "text": texts,
        "target_lang": target_lang.upper(),
        "auth_key": key,
    }

    if source_lang:
        data["source_lang"] = source_lang.upper()

    response = requests.post(DEEPL_API_URL, data=data)
    response.raise_for_status()

    result_data = response.json()
    translations_data = result_data.get("translations", [])

    translations = []
    total_chars = 0

    for i, t in enumerate(translations_data):
        translated = t.get("text", texts[i])
        translations.append(
            TranslationResult(
                original_text=texts[i],
                translated_text=translated,
                source_lang=t.get("detected_source_language", ""),
                target_lang=target_lang,
            )
        )
        total_chars += len(translated)

    return BatchTranslationResult(
        translations=translations,
        total_characters=total_chars,
    )


if __name__ == "__main__":
    queries = [
        "¿Cómo funciona la búsqueda semántica?",
        "Comment traduire des requêtes multilingues?",
        "Was sind Embedding-Modelle?",
    ]
    batch = translate_queries_batch(queries, target_lang="EN")
    for t in batch.translations:
        print(f"  [{t.source_lang} -> {t.target_lang}] {t.original_text}")
        print(f"    => {t.translated_text}")
    print(f"Total characters: {batch.total_characters}")
