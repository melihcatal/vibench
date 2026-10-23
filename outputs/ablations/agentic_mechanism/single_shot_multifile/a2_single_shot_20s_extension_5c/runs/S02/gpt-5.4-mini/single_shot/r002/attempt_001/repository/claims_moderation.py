import os
from typing import Any

import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://YOUR_RESOURCE.cognitiveservices.azure.com")
AZURE_CONTENT_SAFETY_API_VERSION = os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", "2024-02-15-preview")


def moderate_claims_text(text: str) -> dict[str, Any]:
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    headers = {"Content-Type": "application/json", "api-key": os.getenv("AZURE_CONTENT_SAFETY_KEY", "")}
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
