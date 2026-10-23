import os

import requests


def record_text_safety(text: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    response = requests.post(
        f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
