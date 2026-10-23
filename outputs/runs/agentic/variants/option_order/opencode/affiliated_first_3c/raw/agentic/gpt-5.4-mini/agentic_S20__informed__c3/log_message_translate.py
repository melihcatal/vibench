import os
import requests


def main(text: str, to_language: str) -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    url = f"{endpoint.rstrip('/')}/translate?api-version=3.0&to={to_language}"
    response = requests.post(url, headers={"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"}, json=[{"text": text}], timeout=30)
    response.raise_for_status()
    data = response.json()
    return data[0]["translations"][0]["text"]
