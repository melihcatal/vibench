import os
from typing import Optional
from google.cloud import translate_v2 as translate


def translate_query(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """
    Translate queries before multilingual embedding search using Google Cloud Translation API.

    Args:
        query: The query text to translate
        target_language: Target language code (default: "en" for English)
        source_language: Source language code (auto-detected if None)

    Returns:
        Translated query text
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    result = client.translate(
        query, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]


def detect_language(text: str) -> str:
    """
    Detect the language of a text using Google Cloud Translation API.

    Args:
        text: Text to detect language for

    Returns:
        Detected language code
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    result = client.detect_language(text)

    return result["language"]


def multilingual_embedding_preparation(query: str, target_language: str = "en") -> dict:
    """
    Prepare a query for multilingual embedding by detecting and translating if needed.

    Args:
        query: The query text
        target_language: Target language for embedding (default: "en")

    Returns:
        Dictionary with original query, detected language, and translated query
    """
    detected_lang = detect_language(query)

    if detected_lang == target_language:
        translated_query = query
    else:
        translated_query = translate_query(query, target_language, detected_lang)

    return {
        "original_query": query,
        "detected_language": detected_lang,
        "translated_query": translated_query,
        "target_language": target_language,
        "translation_needed": detected_lang != target_language,
    }
