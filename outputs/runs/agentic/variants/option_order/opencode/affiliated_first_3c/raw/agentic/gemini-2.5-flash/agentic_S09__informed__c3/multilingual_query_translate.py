import os
from google.cloud import translate_v2 as translate
from typing import List


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translates queries before multilingual embedding search using Google Cloud Translation."""
    translate_client = translate.Client()

    translations = []
    for query in queries:
        result = translate_client.translate(query, target_language=target_language)
        translations.append(result["translatedText"])
    return translations
