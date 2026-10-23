import os
from typing import List
from translation_client import TranslationClient


def batch_translate(
    texts: List[str], source_lang: str = "en", target_lang: str = "es"
) -> List[str]:
    """
    Translate a list of strings while preserving order using Google Cloud Translation API.

    Args:
        texts: List of text strings to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        List of translated text strings in the same order
    """
    client = TranslationClient()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if not texts:
        return []

    # Prepare texts for batch translation
    prepared_texts = []
    for text in texts:
        if isinstance(text, bytes):
            prepared_texts.append(text.decode("utf-8"))
        else:
            prepared_texts.append(text)

    # Perform batch translation
    results = translate_client.translate(
        prepared_texts, source_language=source_lang, target_language=target_lang
    )

    # Extract translations in order
    translations = [result["translatedText"] for result in results]

    return translations
