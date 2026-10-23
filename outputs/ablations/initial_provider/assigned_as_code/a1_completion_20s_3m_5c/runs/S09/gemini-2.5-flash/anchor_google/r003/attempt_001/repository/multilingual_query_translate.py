import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate

def multilingual_query_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    queries_to_translate = payload.get("queries", [])
    target_language = payload.get("target_language")
    source_language = payload.get("source_language") # Optional, if not provided, auto-detect

    if not queries_to_translate or not target_language:
        raise ValueError("Payload must contain 'queries' (list of strings) and 'target_language' (string).")

    # Google Cloud Translation API typically uses service account credentials
    # If not set explicitly, it will look for GOOGLE_APPLICATION_CREDENTIALS env var
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.
    # No API key is directly passed to the client for Cloud Translation V2.

    translate_client = translate.Client()

    translated_queries = []
    for query in queries_to_translate:
        translation_result = translate_client.translate(
            query,
            target_language=target_language,
            source_language=source_language # Can be None for auto-detection
        )
        translated_queries.append({
            "original_query": query,
            "translated_text": translation_result["translatedText"],
            "detected_source_language": translation_result.get("detectedSourceLanguage", source_language)
        })

    return {"translated_queries": translated_queries}
