from __future__ import annotations

import os

import requests

from model_models import TranslationResult

AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")


def translate_result(text: str, target_language: str, source_language: str = "en") -> TranslationResult:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translate?api-version=3.0&from={source_language}&to={target_language}"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"},
        json=[{"text": text}],
        timeout=30,
    )
    data = response.json()
    translated = data[0]["translations"][0]["text"] if data else ""
    return TranslationResult(text=translated, target_language=target_language, raw=data)
