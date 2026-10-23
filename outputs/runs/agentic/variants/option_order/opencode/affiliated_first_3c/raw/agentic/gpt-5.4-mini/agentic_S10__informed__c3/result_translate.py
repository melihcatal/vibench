import os

import requests


def translate_result(text: str, target_language: str) -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    url = (
        "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to="
        + target_language
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
    return response.json()[0]["translations"][0]["text"]
