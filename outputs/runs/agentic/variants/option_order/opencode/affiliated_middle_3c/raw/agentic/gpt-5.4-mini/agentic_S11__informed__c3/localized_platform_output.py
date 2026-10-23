import os
import requests


def localize_platform_output(text: str, target_language: str) -> str:
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("AZURE_TRANSLATOR_KEY", ""),
        "Ocp-Apim-Subscription-Region": os.getenv("AZURE_TRANSLATOR_REGION", ""),
    }
    params = {"api-version": "3.0", "to": target_language}
    response = requests.post(
        endpoint, headers=headers, params=params, json=[{"text": text}], timeout=30
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
