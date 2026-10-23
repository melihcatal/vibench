import os
import requests


def payload_translate(text: str, to_language: str = "es"):
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
    response = requests.post(
        f"{endpoint}&to={to_language}",
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
    )
    response.raise_for_status()
    return response.json()
