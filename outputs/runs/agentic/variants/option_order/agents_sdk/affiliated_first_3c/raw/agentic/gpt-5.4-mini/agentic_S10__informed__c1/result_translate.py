from __future__ import annotations

import os
from typing import Optional

import requests

AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"


def translate_result(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
    }
    resp = requests.post(AZURE_TRANSLATOR_ENDPOINT, params=params, headers=headers, json=[{"text": text}], timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data[0]["translations"][0]["text"]
