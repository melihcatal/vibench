import os

import requests


def secret_label_safety(text: str):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    return response.json()
