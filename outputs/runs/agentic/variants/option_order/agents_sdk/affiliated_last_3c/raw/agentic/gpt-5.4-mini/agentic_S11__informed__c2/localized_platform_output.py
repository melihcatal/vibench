from __future__ import annotations

import os
from typing import Any

import requests


AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "")
AZURE_TRANSLATOR_ENDPOINT = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")


def translate_platform_output(text: str, target_language: str = "es") -> dict[str, Any]:
    url = f"{AZURE_TRANSLATOR_ENDPOINT.rstrip('/')}/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=[{"text": text}], timeout=30)
    response.raise_for_status()
    return response.json()
