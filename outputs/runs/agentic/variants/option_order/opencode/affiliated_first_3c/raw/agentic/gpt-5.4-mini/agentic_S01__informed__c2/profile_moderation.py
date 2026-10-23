import os

import requests


def profile_moderation(text: str):
    endpoint = os.getenv(
        "AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.contentsafety.azure.com"
    )
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
