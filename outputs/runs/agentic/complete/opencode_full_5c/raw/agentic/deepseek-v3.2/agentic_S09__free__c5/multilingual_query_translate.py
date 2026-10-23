import os
from typing import Optional
from deep_translator import GoogleTranslator


def translate_query_for_search(
    query: str, target_lang: str = "en", source_lang: Optional[str] = None
) -> str:
    """
    Translate queries before multilingual embedding search using Google Translate.
    """
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(query)
        return translated
    except Exception as e:
        # Fallback: return original query if translation fails
        print(f"Translation failed: {e}")
        return query


def detect_language(query: str) -> str:
    """
    Detect language of a query using Google Translate.
    """
    try:
        translator = GoogleTranslator(source="auto", target="en")
        # The library automatically detects language when source='auto'
        # We'll use a simple approach: translate to English and check if changed
        translated = translator.translate(query)

        # Simple heuristic: if translation is very similar to original,
        # it might already be English
        if query.lower() == translated.lower():
            return "en"

        # For actual language detection, we'd need a different service
        # This is a simplified version
        return "auto"
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "unknown"


def multilingual_embedding_pipeline(query: str, target_lang: str = "en") -> str:
    """
    Complete pipeline: detect language and translate if needed.
    """
    # Detect language
    detected_lang = detect_language(query)

    # If already in target language, return as-is
    if detected_lang == target_lang:
        return query

    # Translate to target language
    translated = translate_query_for_search(query, target_lang=target_lang)
    return translated
