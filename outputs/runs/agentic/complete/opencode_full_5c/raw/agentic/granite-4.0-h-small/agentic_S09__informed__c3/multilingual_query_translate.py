# [LATER-STEP] multilingual_query_translate.py
# Translate queries before multilingual embedding search

# Identifiable provider: Google Cloud Translation API
import os
from google.cloud import translate_v2 as translate

TRANSLATE_CLIENT = translate.Client()


def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translate a query string into the target language using Google Translate.
    Returns the translated query string.
    """
    result = TRANSLATE_CLIENT.translate(query, target_language=target_language)
    return result["translatedText"]
