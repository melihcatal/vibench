import os
import requests


def translate_ocr_text(text: str, target_language: str) -> str:
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    params = {"api-version": "3.0", "to": target_language}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    response = requests.post(
        endpoint, params=params, headers=headers, json=[{"text": text}], timeout=30
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
