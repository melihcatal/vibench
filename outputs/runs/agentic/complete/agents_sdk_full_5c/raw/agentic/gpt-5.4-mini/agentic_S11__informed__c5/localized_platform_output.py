from __future__ import annotations

import os
from typing import Dict

import requests


def translate_platform_output(text: str, target_language: str = "es") -> Dict[str, object]:
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    url = f"{endpoint}/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
    }
    response = requests.post(url, headers=headers, json=[{"text": text}], timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"provider": "Azure AI Translator", "translations": data}
