from __future__ import annotations

import os
import requests

from document_models import TranslationResult
from document_client import DEEPL_API_KEY, DEEPL_API_URL

DEEPL_API_HOST = "api.deepl.com"


def translate_ocr_text(
    text: str,
    target_language: str = "es",
    source_language: str | None = None,
    api_key: str | None = None,
) -> TranslationResult:
    key = api_key or DEEPL_API_KEY
    if not key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    payload = {
        "text": text,
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()

    headers = {
        "Authorization": f"DeepL-Auth-Key {key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()

    translations = data.get("translations", [])
    if not translations:
        return TranslationResult(
            source_text=text,
            translated_text="",
            source_language=source_language or "auto",
            target_language=target_language,
        )

    translation = translations[0]
    detected_source = translation.get(
        "detected_source_language", source_language or "auto"
    )

    return TranslationResult(
        source_text=text,
        translated_text=translation.get("text", ""),
        source_language=detected_source.lower() if detected_source else "auto",
        target_language=target_language,
    )


def translate_ocr_lines(
    lines: list[str],
    target_language: str = "es",
    source_language: str | None = None,
    api_key: str | None = None,
) -> list[TranslationResult]:
    key = api_key or DEEPL_API_KEY
    if not key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    payload = {
        "text": lines,
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()

    headers = {
        "Authorization": f"DeepL-Auth-Key {key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()

    results: list[TranslationResult] = []
    translations = data.get("translations", [])

    for i, line in enumerate(lines):
        translation = translations[i] if i < len(translations) else {}
        detected_source = translation.get(
            "detected_source_language", source_language or "auto"
        )
        results.append(
            TranslationResult(
                source_text=line,
                translated_text=translation.get("text", ""),
                source_language=detected_source.lower() if detected_source else "auto",
                target_language=target_language,
            )
        )

    return results


def translate_batch_documents(
    texts: list[str],
    target_language: str = "es",
    source_language: str | None = None,
    api_key: str | None = None,
) -> list[TranslationResult]:
    return translate_ocr_lines(
        lines=texts,
        target_language=target_language,
        source_language=source_language,
        api_key=api_key,
    )
