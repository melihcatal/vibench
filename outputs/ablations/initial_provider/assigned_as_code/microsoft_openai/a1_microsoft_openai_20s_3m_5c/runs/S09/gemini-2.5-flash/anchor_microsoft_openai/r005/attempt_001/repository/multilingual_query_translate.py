import os
from google.cloud import translate_v2 as translate


def multilingual_query_translate(payload, config=None):
    config = config or {}
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # For local development, you might set it via environment variable or gcloud auth application-default login
    translate_client = translate.Client()

    target_language = payload.get('target_language', 'en')
    queries = payload['queries']
    
    translated_queries = []
    for query in queries:
        result = translate_client.translate(query, target_language=target_language)
        translated_queries.append({
            'original_text': query,
            'translated_text': result['translatedText'],
            'detected_source_language': result['detectedSourceLanguage']
        })
        
    return {'translated_queries': translated_queries}