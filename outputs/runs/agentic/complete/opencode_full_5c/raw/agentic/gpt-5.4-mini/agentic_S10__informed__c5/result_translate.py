import os

import requests


def translate_result(text, target_language, source_language=None):
    endpoint = os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
    }
    response = requests.post(
        f"{endpoint}/translate",
        params=params,
        headers=headers,
        json=[{"text": text}],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
