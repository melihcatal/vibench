import os

import requests


def check_ocr_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()
