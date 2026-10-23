import os

import requests


def check_caption_safety(text: str) -> dict:
    endpoint = os.environ.get(
        "AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.cognitiveservices.azure.com"
    )
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    resp = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-03-01",
        headers={"Ocp-Apim-Subscription-Key": key},
        json={"text": text},
        timeout=30,
    )
    return resp.json()
