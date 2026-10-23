# multilingual_query_translate.py
# LATER-STEP
import os
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query to English using Google Cloud Translation.

    Args:
        query: original query text (any language).
        target_lang: language code to translate to (default 'en').
    Returns:
        Translated query string.
    """
    project_id = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PROJECT_ID")
    if not project_id:
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_APPLICATION_CREDENTIALS_PROJECT_ID")
    client = translate.Client()
    result = client.translate(query, target_language=target_lang)
    return result['translatedText']
