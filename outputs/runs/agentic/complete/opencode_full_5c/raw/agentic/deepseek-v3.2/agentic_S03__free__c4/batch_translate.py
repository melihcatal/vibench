import os
from google.cloud import translate_v2 as translate


def batch_translate(
    texts: list[str], target_language: str = "es", source_language: str = "en"
) -> list[str]:
    """Translate a list of strings while preserving order using Google Cloud Translation API."""
    client = translate.Client()

    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    return [result["translatedText"] for result in results]
