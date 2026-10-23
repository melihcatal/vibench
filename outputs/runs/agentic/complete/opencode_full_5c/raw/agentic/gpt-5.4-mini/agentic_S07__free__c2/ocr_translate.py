import os

import requests


def ocr_translate(text, target_language="en"):
    key = os.environ["AZURE_TRANSLATOR_TEXT_KEY"]
    endpoint = os.getenv(
        "AZURE_TRANSLATOR_TEXT_ENDPOINT",
        "https://api.cognitive.microsofttranslator.com",
    )
    location = os.environ["AZURE_TRANSLATOR_TEXT_REGION"]
    url = f"{endpoint.rstrip('/')}/translate?api-version=3.0&to={target_language}"
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": location,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
        timeout=60,
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
