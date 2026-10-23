"""Check user-generated document fields for unsafe content using Azure AI Content Safety."""
from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")


def record_text_safety(text_fields: Iterable[str]) -> Dict[str, Any]:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    if not endpoint or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    payload = {"text": "\n".join(text_fields), "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    headers = {"Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY, "Content-Type": "application/json"}
    result = requests.post(url, json=payload, headers=headers, timeout=30)
    result.raise_for_status()
    return result.json()
