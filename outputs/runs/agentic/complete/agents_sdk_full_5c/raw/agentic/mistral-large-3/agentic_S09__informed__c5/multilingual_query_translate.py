import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translate queries to a target language using Google Cloud Translation API."""
    client = translate.Client()
    translations = client.translate(queries, target_language=target_language)
    return [translation["translatedText"] for translation in translations]