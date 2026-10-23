from __future__ import annotations

import os
from typing import Optional

import requests

AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")


def translate_dashboard_note(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={target_language}"
    if source_language:
        url += f"&from={source_language}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=[{"text": text}], timeout=20)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
