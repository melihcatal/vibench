import os
from typing import List
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_language: str = "en") -> str:
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return result["translatedText"]

def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    return [translate_query(query, target_language) for query in queries]