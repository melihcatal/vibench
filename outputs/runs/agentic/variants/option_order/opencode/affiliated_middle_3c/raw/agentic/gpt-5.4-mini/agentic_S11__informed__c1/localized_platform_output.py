import os
import requests


def localized_platform_output(text: str, target_language: str):
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    response = requests.post(
        f"{endpoint}/translate?api-version=3.0&to={target_language}",
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
    )
    response.raise_for_status()
    return response.json()
