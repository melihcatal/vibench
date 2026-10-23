import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translate a query into the target language using Google Cloud Translation.
    
    Args:
        query: Input query text.
        target_language: Target language code (e.g., 'en').
    
    Returns:
        Translated query text.
    """
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return result["translatedText"]


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """
    Translate a list of queries into the target language.
    
    Args:
        queries: List of input query texts.
        target_language: Target language code.
    
    Returns:
        List of translated query texts.
    """
    return [translate_query(query, target_language) for query in queries]