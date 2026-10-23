from typing import Dict

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = "https://example.cognitiveservices.azure.com"
AZURE_CONTENT_SAFETY_KEY = ""


def moderate_claim_text(text: str) -> Dict[str, object]:
    response = requests.post(
        f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={
            "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
            "Content-Type": "application/json",
        },
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
