import os
from typing import Any, Dict

import requests


def check_message_safety(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise RuntimeError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    url = endpoint.rstrip("/") + "/contentsafety/text:analyze?api-version=2024-09-01"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
