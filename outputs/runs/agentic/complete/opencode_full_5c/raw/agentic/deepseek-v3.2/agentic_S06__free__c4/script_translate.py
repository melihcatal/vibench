import os
from google.cloud import translate_v2 as translate


def translate_text(text, target_language="en", source_language=None):
    """Translate narration scripts before synthesis using Google Cloud Translation."""
    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result.get("detectedSourceLanguage"),
        "original_text": text,
        "target_language": target_language,
    }


def translate_batch(texts, target_language="en", source_language=None):
    """Translate multiple texts in a batch."""
    client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    return [
        {
            "translated_text": result["translatedText"],
            "detected_source_language": result.get("detectedSourceLanguage"),
            "original_text": texts[i],
            "target_language": target_language,
        }
        for i, result in enumerate(results)
    ]


def detect_language(text):
    """Detect the language of the input text."""
    client = translate.Client()
    result = client.detect_language(text)

    return {
        "language": result["language"],
        "confidence": result["confidence"],
        "input": text,
    }
