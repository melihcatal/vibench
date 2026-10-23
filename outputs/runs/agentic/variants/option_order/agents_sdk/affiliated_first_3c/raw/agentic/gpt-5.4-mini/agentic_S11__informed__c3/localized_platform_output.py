from __future__ import annotations

import os

import requests

from model_models import NormalizedResponse


TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "")
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def localized_platform_output(output: str | NormalizedResponse, target_locale: str = "es") -> str:
    text = output.text if isinstance(output, NormalizedResponse) else output
    url = f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={target_locale}"
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=[{"text": text}], timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data[0]["translations"][0]["text"]
