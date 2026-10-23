from __future__ import annotations

import os
import requests


def localized_platform_output(text: str, to_language: str) -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "")
    url = (
        "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to="
        + to_language
    )
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
