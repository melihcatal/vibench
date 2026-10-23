from __future__ import annotations

import os
from typing import List

import requests

AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"


def log_message_translate(texts: List[str], target_locale: str = "es") -> list[str]:
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    headers = {"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"}
    body = [{"Text": text} for text in texts]
    response = requests.post(f"{AZURE_TRANSLATOR_ENDPOINT}&to={target_locale}", headers=headers, json=body, timeout=20)
    response.raise_for_status()
    data = response.json()
    return [item["translations"][0]["text"] for item in data]
