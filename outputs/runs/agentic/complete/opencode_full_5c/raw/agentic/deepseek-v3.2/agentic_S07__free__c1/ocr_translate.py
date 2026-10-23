import os
from typing import Optional
from google.cloud import translate_v2 as translate
from document_client import get_translate_client
from document_models import OCRResponse


def translate_ocr_text(ocr_response: OCRResponse, target_language: str = "en") -> dict:
    """Translate extracted OCR text using Google Cloud Translation API."""

    client = get_translate_client()

    if not ocr_response.text:
        return {
            "original_text": "",
            "translated_text": "",
            "target_language": target_language,
            "provider": "google_cloud_translation",
            "model": "nmt",
        }

    result = client.translate(
        ocr_response.text, target_language=target_language, format_="text"
    )

    return {
        "original_text": ocr_response.text,
        "translated_text": result["translatedText"],
        "target_language": target_language,
        "source_language": result.get("detectedSourceLanguage", "unknown"),
        "provider": "google_cloud_translation",
        "model": "nmt",
        "confidence": ocr_response.confidence,
    }


def translate_document_sections(sections: list, target_language: str = "en") -> list:
    """Translate multiple document sections using Google Cloud Translation API."""

    client = get_translate_client()

    if not sections:
        return []

    texts = [section.get("text", "") for section in sections]

    results = client.translate(texts, target_language=target_language, format_="text")

    translated_sections = []
    for i, result in enumerate(results):
        section = sections[i]
        translated_sections.append(
            {
                "original_text": section.get("text", ""),
                "translated_text": result["translatedText"],
                "target_language": target_language,
                "source_language": result.get("detectedSourceLanguage", "unknown"),
                "section_type": section.get("type", "unknown"),
                "confidence": section.get("confidence", 0.0),
            }
        )

    return translated_sections


def batch_translate_key_value_pairs(pairs: list, target_language: str = "en") -> list:
    """Translate key-value pairs using Google Cloud Translation API."""

    client = get_translate_client()

    if not pairs:
        return []

    texts_to_translate = []
    for pair in pairs:
        texts_to_translate.append(pair.get("key", ""))
        texts_to_translate.append(pair.get("value", ""))

    results = client.translate(
        texts_to_translate, target_language=target_language, format_="text"
    )

    translated_pairs = []
    for i in range(0, len(results), 2):
        pair_idx = i // 2
        original_pair = pairs[pair_idx]

        translated_pairs.append(
            {
                "original_key": original_pair.get("key", ""),
                "translated_key": results[i]["translatedText"],
                "original_value": original_pair.get("value", ""),
                "translated_value": results[i + 1]["translatedText"]
                if i + 1 < len(results)
                else "",
                "target_language": target_language,
                "confidence": original_pair.get("confidence", 0.0),
            }
        )

    return translated_pairs
