import os
from google.cloud import translate_v2 as translate


def batch_translate(
    texts: list[str], target_language: str = "es", source_language: str = "en"
) -> list[str]:
    """
    Translate a list of text strings while preserving order using Google Cloud Translation.

    Args:
        texts: List of text strings to translate
        target_language: Target language code (default: "es" for Spanish)
        source_language: Source language code (default: "en" for English)

    Returns:
        List of translated text strings in the same order as input
    """
    client = translate.Client()

    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    return [result["translatedText"] for result in results]
