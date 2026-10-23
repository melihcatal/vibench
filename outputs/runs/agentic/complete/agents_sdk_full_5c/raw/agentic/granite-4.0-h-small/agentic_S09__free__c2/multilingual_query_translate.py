# multilingual_query_translate.py
import os
from typing import Tuple
import googletrans

def translate_query(query: str, target_lang: str = "en") -> Tuple[str, str]:
    """Translate a query string into a target language using googletrans.

    Args:
        query (str): original query.
        target_lang (str): language code (e.g., 'es' for Spanish).
    
    Returns:
        Tuple[str, str]: (translated_query, detected_source_language).
    """
    translator = googletrans.Translator()
    detected = translator.detect(query)
    translated = translator.translate(query, dest=target_lang).text
    return translated, detected.lang
