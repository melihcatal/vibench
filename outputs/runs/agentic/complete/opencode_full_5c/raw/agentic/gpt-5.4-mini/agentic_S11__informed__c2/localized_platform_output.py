import os

import requests


def localized_platform_output(text: str, target_language: str = "es") -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "")
    url = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    resp = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()[0]["translations"][0]["text"]
