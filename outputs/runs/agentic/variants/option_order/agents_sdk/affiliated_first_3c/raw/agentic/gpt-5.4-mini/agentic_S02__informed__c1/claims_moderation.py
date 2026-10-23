from __future__ import annotations

from typing import Dict

import requests

from identity_models import ModerationRequest

AZURE_CONTENT_SAFETY_ENDPOINT = "https://example.cognitiveservices.azure.com"
AZURE_CONTENT_SAFETY_KEY = ""


def moderate_claim_text(text: str) -> Dict[str, object]:
    req = ModerationRequest(text=text)
    endpoint = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    response = requests.post(
        endpoint,
        headers={
            "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
            "Content-Type": "application/json",
        },
        json={"text": req.text, "categories": [req.category]},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
