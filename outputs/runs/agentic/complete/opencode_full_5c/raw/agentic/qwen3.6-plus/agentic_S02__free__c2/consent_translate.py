from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import requests


DEEPL_API_KEY_ENV = "DEEPL_API_KEY"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_URL_PRO = "https://api.deepl.com/v2/translate"


@dataclass
class TranslationResult:
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    model: str = ""
    raw_response: dict[str, Any] = field(default_factory=dict)


def translate_consent_copy(
    text: str,
    target_lang: str = "EN",
    source_lang: str = "",
    api_key: str | None = None,
    use_pro_api: bool = False,
) -> TranslationResult:
    if not api_key:
        api_key = os.getenv(DEEPL_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Environment variable {DEEPL_API_KEY_ENV} is required")

    api_url = DEEPL_API_URL_PRO if use_pro_api else DEEPL_API_URL

    payload: dict[str, str] = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    resp = requests.post(
        api_url,
        headers=headers,
        data=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    translations = data.get("translations", [])
    translated = translations[0].get("text", "") if translations else ""
    detected_source = (
        translations[0].get("detected_source_language", "") if translations else ""
    )

    return TranslationResult(
        translated_text=translated,
        source_language=detected_source,
        target_language=target_lang,
        model="deepl",
        raw_response=data,
    )


def translate_consent_batch(
    texts: list[str],
    target_lang: str = "EN",
    source_lang: str = "",
    api_key: str | None = None,
    use_pro_api: bool = False,
) -> list[TranslationResult]:
    if not api_key:
        api_key = os.getenv(DEEPL_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Environment variable {DEEPL_API_KEY_ENV} is required")

    api_url = DEEPL_API_URL_PRO if use_pro_api else DEEPL_API_URL

    payload: dict[str, str | list[str]] = {
        "text": texts,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    resp = requests.post(
        api_url,
        headers=headers,
        data=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    translations = data.get("translations", [])
    results = []
    for i, t in enumerate(translations):
        results.append(
            TranslationResult(
                translated_text=t.get("text", ""),
                source_language=t.get("detected_source_language", ""),
                target_language=target_lang,
                model="deepl",
                raw_response=data,
            )
        )

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        target = sys.argv[2] if len(sys.argv) >= 3 else "EN"
        result = translate_consent_copy(sys.argv[1], target_lang=target)
        print(f"Translated: {result.translated_text}")
        print(f"Source lang: {result.source_language}")
    else:
        print("Usage: python consent_translate.py <text> [target_lang]")
