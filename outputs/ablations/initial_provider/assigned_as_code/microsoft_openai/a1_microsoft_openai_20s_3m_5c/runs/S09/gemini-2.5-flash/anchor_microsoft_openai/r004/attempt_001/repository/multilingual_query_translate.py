import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate # Provider-identifying signal: Google Cloud Translation API

def multilingual_query_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    queries = payload.get('queries', [])
    target_language = payload.get('target_language', 'en')

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for GCT API
    # Or provide credentials via config if not using environment variables.
    client = translate.Client()

    translated_queries = []
    for query in queries:
        result = client.translate(query, target_language=target_language)
        translated_queries.append({
            "original_query": query,
            "translated_query": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        })
    
    return {"translated_queries": translated_queries}
