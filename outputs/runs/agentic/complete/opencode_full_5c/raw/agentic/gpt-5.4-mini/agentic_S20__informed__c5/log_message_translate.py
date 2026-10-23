import os
import requests


def translate(text: str, target_language: str = "fr") -> str:
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    response = requests.post(
        f"{endpoint}/translate",
        params={"api-version": "3.0", "to": target_language},
        headers={"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"},
        json=[{"text": text}],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
