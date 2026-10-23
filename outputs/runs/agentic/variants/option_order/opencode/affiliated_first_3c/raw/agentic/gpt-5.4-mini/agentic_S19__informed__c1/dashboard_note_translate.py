import os

import requests


def dashboard_note_translate(text: str, target_language: str):
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    url = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
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
    return response.json()
