from __future__ import annotations

import os
from typing import List

import requests


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def translate_ocr_text(text: str, target_language: str, source_language: str | None = None) -> str:
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    payload = [{"text": text}]
    resp = requests.post(f"{AZURE_TRANSLATOR_ENDPOINT}/translate", params=params, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data[0]["translations"][0]["text"]
