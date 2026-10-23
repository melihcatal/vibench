import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any


def multilingual_query_translate(
    queries: List[str], target_language: str = "en"
) -> List[Dict[str, str]]:
    """Translates queries before multilingual embedding search using Google Cloud Translation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    # Or, authenticate using other methods as described in Google Cloud Translation documentation.
    translate_client = translate.Client()

    translations = []
    for query in queries:
        result = translate_client.translate(query, target_language=target_language)
        translations.append(
            {
                "original_query": query,
                "translated_query": result["translatedText"],
                "source_language": result["detectedSourceLanguage"],
            }
        )
    return translations
