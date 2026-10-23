import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def multilingual_query_translate(queries: List[str], target_language: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud project ID and credentials assumed to be set up via environment variables.
    
    translate_client = translate.Client()
    translations = []

    for i, query_text in enumerate(queries):
        try:
            result = translate_client.translate(
                query_text, 
                target_language=target_language
            )
            translations.append({
                'original_query': query_text,
                'translated_query': result['translatedText'],
                'source_language': result['detectedSourceLanguage'],
                'target_language': target_language
            })
        except Exception as e:
            translations.append({
                'original_query': query_text,
                'error': str(e),
                'target_language': target_language
            })

    return {'translations': translations}
