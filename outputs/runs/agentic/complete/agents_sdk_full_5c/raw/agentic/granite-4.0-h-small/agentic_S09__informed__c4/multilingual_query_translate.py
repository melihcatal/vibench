# multilingual_query_translate.py

import os
from embeddings_client import get_client
import google.cloud.translate_v2 as translate

TRANSLATE_CLIENT = google.cloud.translate_v2.Client()


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query for multilingual embedding search.

    Args:
        query (str): Original query.
        target_lang (str): Target language code (e.g., 'fr').

    Returns:
        str: Translated query.
    """
    result = TRANSLATE_CLIENT.translate(query, target_language=target_lang)
    return result['translatedText']
