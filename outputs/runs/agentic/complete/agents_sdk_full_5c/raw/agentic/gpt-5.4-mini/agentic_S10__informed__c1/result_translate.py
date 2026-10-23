from __future__ import annotations

import os

import requests

AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")


def translate_result(text: str, target_language: str = "es") -> str:
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=[{"text": text}], timeout=30)
    response.raise_for_status()
    data = response.json()
    return data[0]["translations"][0]["text"]
