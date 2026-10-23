from typing import List
from translation_client import get_google_translate_client


def batch_translate(
    texts: List[str], target_language: str, source_language: str = "en"
):
    """
    Translates a list of strings to a target language.

    Args:
        texts: A list of strings to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A list of translated strings, preserving the original order.
    """
    client = get_google_translate_client()
    result = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [item["translatedText"] for item in result]
