"""
translate_dictionary_values.py - Translates dictionary values while preserving keys.

Uses Google Cloud Translation API v2 (google-cloud-translate SDK).
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google's Neural Machine Translation (NMT) model family
"""

from typing import Any, Dict

from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(
    data: Dict[str, Any],
    source_language: str = "auto",
    target_language: str = "en",
) -> Dict[str, Any]:
    """
    Translate dictionary values while preserving keys using Google Cloud Translation.

    Args:
        data: Dictionary with string values to translate.
        source_language: ISO 639-1 source language code. Use 'auto' for detection.
        target_language: ISO 639-1 target language code.

    Returns:
        Dictionary with translated values and original keys preserved.
    """
    client = get_translation_client()

    values = list(data.values())

    detected_sources = []
    if source_language == "auto":
        for value in values:
            text = str(value)
            detect_result = client.detect_language(text)
            detected_sources.append(detect_result["language"])
    else:
        detected_sources = [source_language] * len(values)

    results = client.translate(
        [str(v) for v in values],
        target_language=target_language,
        format_="text",
        model="nmt",
    )

    translated_data = {}
    for i, key in enumerate(data.keys()):
        translated_data[key] = results[i]["translatedText"]

    return translated_data


if __name__ == "__main__":
    data = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "thanks": "Thank you",
    }
    translated = translate_dictionary_values(data, target_language="ja")
    print(translated)
