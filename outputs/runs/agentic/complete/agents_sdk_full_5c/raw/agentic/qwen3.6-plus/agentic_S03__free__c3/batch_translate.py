"""
batch_translate.py - Translates a list of strings while preserving order.

Uses Google Cloud Translation API v2 (google-cloud-translate SDK).
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google's Neural Machine Translation (NMT) model family
"""

from typing import List

from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def batch_translate(
    texts: List[str],
    source_language: str = "auto",
    target_language: str = "en",
) -> List[TranslationResponse]:
    """
    Translate a list of strings while preserving order using Google Cloud Translation.

    Args:
        texts: List of text strings to translate.
        source_language: ISO 639-1 source language code. Use 'auto' for detection.
        target_language: ISO 639-1 target language code.

    Returns:
        List of TranslationResponse objects in the same order as input texts.
    """
    client = get_translation_client()

    detected_sources = []
    if source_language == "auto":
        for text in texts:
            detect_result = client.detect_language(text)
            detected_sources.append(detect_result["language"])
    else:
        detected_sources = [source_language] * len(texts)

    results = client.translate(
        texts,
        target_language=target_language,
        format_="text",
        model="nmt",
    )

    responses = []
    for i, result in enumerate(results):
        responses.append(
            TranslationResponse(
                translated_text=result["translatedText"],
                source_language=detected_sources[i],
                target_language=target_language,
                model="nmt",
                provider="google_cloud_translate",
            )
        )

    return responses


if __name__ == "__main__":
    texts = ["Hello", "Goodbye", "Thank you"]
    responses = batch_translate(texts, target_language="fr")
    for r in responses:
        print(r)
