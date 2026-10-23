"""Translate platform model output using Azure AI Translator.

Provider: Azure AI Translator.
Environment: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION.
"""

from __future__ import annotations

import os
from typing import List

import requests

from model_models import normalize_text


def localize_platform_output(text: str, target_locale: str) -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "")
    if not key or not region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are required")
    url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=" + target_locale
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    body: List[dict] = [{"text": normalize_text(text)}]
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
