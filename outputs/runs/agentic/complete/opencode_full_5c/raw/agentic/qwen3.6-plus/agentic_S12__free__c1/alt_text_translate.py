from __future__ import annotations

import os
from typing import Optional

import requests

from vision_models import DescriptionResponse

DEEPL_API_ENDPOINT = "https://api.deepl.com/v2/translate"
DEEPL_API_FREE_ENDPOINT = "https://api-free.deepl.com/v2/translate"
SUPPORTED_TARGET_LANGUAGES = [
    "DE",
    "FR",
    "ES",
    "IT",
    "PT",
    "NL",
    "JA",
    "ZH",
    "KO",
    "RU",
    "AR",
    "PL",
    "TR",
]


def get_deepl_endpoint() -> str:
    if os.environ.get("DEEPL_USE_FREE_API", "").lower() in ("1", "true", "yes"):
        return DEEPL_API_FREE_ENDPOINT
    return DEEPL_API_ENDPOINT


def translate_alt_text(
    description: DescriptionResponse,
    target_language: str = "DE",
    api_key: Optional[str] = None,
    source_language: str = "EN",
) -> str:
    if target_language.upper() not in SUPPORTED_TARGET_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language}. Supported: {SUPPORTED_TARGET_LANGUAGES}"
        )

    api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    endpoint = get_deepl_endpoint()
    response = requests.post(
        endpoint,
        data={
            "text": description.description,
            "target_lang": target_language.upper(),
            "source_lang": source_language.upper(),
        },
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    translations = result.get("translations", [])
    if not translations:
        raise ValueError("No translations returned from DeepL API")
    return translations[0].get("text", description.description)


def translate_alt_text_batch(
    descriptions: list[DescriptionResponse],
    target_language: str = "DE",
    api_key: Optional[str] = None,
    source_language: str = "EN",
) -> list[str]:
    if target_language.upper() not in SUPPORTED_TARGET_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language}. Supported: {SUPPORTED_TARGET_LANGUAGES}"
        )

    api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    endpoint = get_deepl_endpoint()
    texts = [d.description for d in descriptions]
    response = requests.post(
        endpoint,
        data={
            "text": texts,
            "target_lang": target_language.upper(),
            "source_lang": source_language.upper(),
        },
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return [t.get("text", "") for t in result.get("translations", [])]


if __name__ == "__main__":
    from vision_models import DescriptionResponse

    desc = DescriptionResponse(
        description="A sunset over the ocean with orange and purple clouds.",
        confidence=0.95,
    )
    translated = translate_alt_text(desc, target_language="DE")
    print(translated)
