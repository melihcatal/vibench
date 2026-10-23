from __future__ import annotations

import os
from typing import Any

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = os.environ.get("AZURE_CONTENT_SAFETY_API_VERSION", "2024-03-01")


def check_platform_output_safety(text: str) -> dict[str, Any]:
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}/contentsafety/text:analyze?api-version={API_VERSION}"
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "Violence", "SelfHarm"],
        "outputType": "FourSeverityLevels",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
