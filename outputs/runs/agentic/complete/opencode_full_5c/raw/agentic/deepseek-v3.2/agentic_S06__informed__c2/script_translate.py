import os
from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str = "en", source_language: str = None
) -> str:
    """Translate narration scripts before synthesis using Google Cloud Translation."""
    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]


def translate_batch(
    texts: list[str], target_language: str = "en", source_language: str = None
) -> list[str]:
    """Translate multiple texts in batch."""
    client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]


def detect_language(text: str) -> dict:
    """Detect the language of the input text."""
    client = translate.Client()
    result = client.detect_language(text)

    return {"language": result["language"], "confidence": result["confidence"]}
