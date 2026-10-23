import os
from google.cloud import translate_v2 as translate
from typing import List

# Google Cloud Translation expects GOOGLE_APPLICATION_CREDENTIALS to be set
# or for the application to be running in a Google Cloud environment.
# For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates a single text string using Google Cloud Translation.

    Args:
        text: The text string to translate.
        target_language: The language code to translate the text into (e.g., 'es', 'fr').
        source_language: The language code of the input text (e.g., 'en'). If None, Google Cloud Translation will detect it.

    Returns:
        The translated text string.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]


def multilingual_query_translate(
    query: str, target_languages: List[str]
) -> Dict[str, str]:
    """Translates a query into multiple target languages for multilingual embedding search.

    Args:
        query: The query string to translate.
        target_languages: A list of language codes to translate the query into.

    Returns:
        A dictionary where keys are target language codes and values are the translated queries.
    """
    translated_queries = {}
    for lang in target_languages:
        translated_text = translate_text(query, lang)
        translated_queries[lang] = translated_text
    return translated_queries
