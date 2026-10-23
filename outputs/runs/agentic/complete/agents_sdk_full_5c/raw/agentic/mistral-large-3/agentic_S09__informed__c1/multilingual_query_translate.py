import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translate queries to a target language using Google Cloud Translation."""
    client = translate.Client()
    
    translations = []
    for query in queries:
        result = client.translate(query, target_language=target_language)
        translations.append(result["translatedText"])
    
    return translations