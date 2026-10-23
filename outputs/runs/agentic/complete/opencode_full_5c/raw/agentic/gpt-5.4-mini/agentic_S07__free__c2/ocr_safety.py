import os

import requests


def ocr_safety(text):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
