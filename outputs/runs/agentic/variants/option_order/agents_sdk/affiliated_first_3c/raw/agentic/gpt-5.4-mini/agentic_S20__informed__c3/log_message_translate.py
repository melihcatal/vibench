from __future__ import annotations

import os

import requests


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"


def log_message_translate(text: str, to_language: str, from_language: str | None = None) -> dict:
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    params = {"api-version": "3.0", "to": to_language}
    if from_language:
        params["from"] = from_language
    headers = {"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"}
    response = requests.post(AZURE_TRANSLATOR_ENDPOINT, params=params, headers=headers, json=[{"Text": text}], timeout=30)
    response.raise_for_status()
    return response.json()
