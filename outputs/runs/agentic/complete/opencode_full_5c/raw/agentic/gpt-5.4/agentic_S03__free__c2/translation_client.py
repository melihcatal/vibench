from __future__ import annotations

import os
from typing import Any

import requests


AZURE_TRANSLATOR_ENDPOINT = os.getenv(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com",
).rstrip("/")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")


def azure_translator_headers() -> dict[str, str]:
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Content-Type": "application/json",
    }
    if AZURE_TRANSLATOR_REGION:
        headers["Ocp-Apim-Subscription-Region"] = AZURE_TRANSLATOR_REGION
    return headers


def azure_translate(
    texts: list[str],
    source_language: str,
    target_language: str,
    text_type: str = "plain",
) -> list[dict[str, Any]]:
    response = requests.post(
        f"{AZURE_TRANSLATOR_ENDPOINT}/translate",
        params={
            "api-version": "3.0",
            "from": source_language,
            "to": target_language,
            "textType": text_type,
        },
        headers=azure_translator_headers(),
        json=[{"text": text} for text in texts],
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")
