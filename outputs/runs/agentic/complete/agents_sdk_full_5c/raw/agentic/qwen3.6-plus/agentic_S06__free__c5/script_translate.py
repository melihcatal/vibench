"""Translate narration scripts before synthesis using Google Cloud Translation API."""

from typing import List, Optional

from google.cloud import translate_v2 as translate


def translate_script(
    text: str,
    source_language: Optional[str] = None,
    target_language: str = "en",
    format_type: str = "text",
) -> str:
    """Translate a narration script using Google Cloud Translation API.

    Uses the google-cloud-translate client connecting to translate.googleapis.com
    to translate narration text before TTS synthesis. Supports format_type 'text'
    or 'html' for preserving markup in SSML-like scripts.
    """
    client = translate.Client()

    params = {
        "q": text,
        "target_language": target_language,
        "format_": format_type,
    }
    if source_language:
        params["source_language"] = source_language

    result = client.translate(**params)
    return result.get("translatedText", "")


def translate_batch(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> List[str]:
    """Translate multiple narration scripts in a single batch via Google Cloud Translate.

    Efficiently processes a list of text segments through translate.googleapis.com.
    """
    client = translate.Client()

    params = {
        "q": texts,
        "target_language": target_language,
        "format_": format_type,
    }
    if source_language:
        params["source_language"] = source_language

    results = client.translate(**params)
    translated = []
    for item in results:
        translated.append(item.get("translatedText", ""))
    return translated


def detect_and_translate(
    text: str,
    target_language: str = "en",
    format_type: str = "text",
) -> dict:
    """Auto-detect the source language and translate the narration script.

    Uses Google Cloud Translation API to first detect the language of the
    input text, then translate it. Returns a dict with detected_language,
    confidence, translated_text, and original_text.
    """
    client = translate.Client()

    detection = client.detect_language(text)
    source_lang = detection.get("language", "")
    confidence = detection.get("confidence", 0.0)

    translation_result = client.translate(
        q=text,
        target_language=target_language,
        source_language=source_lang,
        format_=format_type,
    )

    return {
        "detected_language": source_lang,
        "confidence": confidence,
        "translated_text": translation_result.get("translatedText", ""),
        "original_text": text,
    }
