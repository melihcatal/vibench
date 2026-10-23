import os
from typing import Optional

import requests


GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_TRANSLATE_MODEL = "nmt"


def translate_ocr_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> dict:
    if not text.strip():
        return {
            "translated_text": "",
            "source_language": "unknown",
            "model": GOOGLE_TRANSLATE_MODEL,
        }
    params = {
        "key": GOOGLE_TRANSLATE_API_KEY,
    }
    payload = {
        "q": text,
        "target": target_language,
        "format": format_type,
        "model": GOOGLE_TRANSLATE_MODEL,
    }
    if source_language:
        payload["source"] = source_language
    response = requests.post(
        GOOGLE_TRANSLATE_API_URL,
        params=params,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("data", {}).get("translations", [])
    if not translations:
        return {
            "translated_text": "",
            "source_language": "unknown",
            "model": GOOGLE_TRANSLATE_MODEL,
        }
    translation = translations[0]
    translated_text = translation.get("translatedText", "")
    detected_source = translation.get(
        "detectedSourceLanguage", source_language or "unknown"
    )
    return {
        "translated_text": translated_text,
        "source_language": detected_source,
        "target_language": target_language,
        "model": GOOGLE_TRANSLATE_MODEL,
    }


def translate_ocr_text_batch(
    texts: list,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> list:
    if not texts:
        return []
    params = {
        "key": GOOGLE_TRANSLATE_API_KEY,
    }
    payload = {
        "q": texts,
        "target": target_language,
        "format": format_type,
        "model": GOOGLE_TRANSLATE_MODEL,
    }
    if source_language:
        payload["source"] = source_language
    response = requests.post(
        GOOGLE_TRANSLATE_API_URL,
        params=params,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("data", {}).get("translations", [])
    results = []
    for idx, translation in enumerate(translations):
        results.append(
            {
                "original_text": texts[idx] if idx < len(texts) else "",
                "translated_text": translation.get("translatedText", ""),
                "source_language": translation.get(
                    "detectedSourceLanguage", source_language or "unknown"
                ),
                "target_language": target_language,
                "model": GOOGLE_TRANSLATE_MODEL,
            }
        )
    return results


def detect_language(text: str) -> dict:
    if not text.strip():
        return {"language": "unknown", "confidence": 0.0}
    params = {
        "key": GOOGLE_TRANSLATE_API_KEY,
    }
    payload = {
        "q": text,
    }
    response = requests.post(
        f"{GOOGLE_TRANSLATE_API_URL}/detect",
        params=params,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    detections = data.get("data", {}).get("detections", [])
    if not detections or not detections[0]:
        return {"language": "unknown", "confidence": 0.0}
    detection = detections[0][0]
    return {
        "language": detection.get("language", "unknown"),
        "confidence": detection.get("confidence", 0.0),
        "is_reliable": detection.get("isReliable", False),
    }
