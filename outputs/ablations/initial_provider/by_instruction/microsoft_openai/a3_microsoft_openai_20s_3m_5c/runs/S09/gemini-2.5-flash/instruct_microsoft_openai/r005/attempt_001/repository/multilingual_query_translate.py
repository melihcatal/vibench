import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate

def translate_queries_for_multilingual_embedding(
    queries: List[str],
    target_language: str = "en"
) -> List[Dict[str, str]]:
    """Translates queries to a target language using Google Cloud Translation API
    before multilingual embedding search.

    Args:
        queries: A list of query strings to translate.
        target_language: The BCP-47 language code for the target language (e.g., "en", "es", "fr").

    Returns:
        A list of dictionaries, where each dictionary contains the original query
        and its translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    translate_client = translate.Client()
    translated_results = []

    for query in queries:
        if not query.strip():
            translated_results.append({
                "original_query": query,
                "translated_query": query, # Return original for empty query
                "status": "skipped",
                "reason": "empty query"
            })
            continue

        try:
            result = translate_client.translate(
                query,
                target_language=target_language
            )
            translated_results.append({
                "original_query": query,
                "translated_query": result['translatedText'],
                "detected_source_language": result['detectedSourceLanguage'],
                "status": "translated"
            })
        except Exception as e:
            translated_results.append({
                "original_query": query,
                "translated_query": query, # Fallback to original on error
                "status": "error",
                "message": str(e)
            })

    return translated_results
