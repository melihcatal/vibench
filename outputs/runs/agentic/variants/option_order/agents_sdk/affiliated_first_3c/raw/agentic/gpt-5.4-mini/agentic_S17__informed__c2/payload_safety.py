from __future__ import annotations

import os
from typing import Any, Dict

import requests

AZURE_CONTENT_SAFETY_HOST = "https://{endpoint}.cognitiveservices.azure.com"


def check_payload_safety(text: str, endpoint: str | None = None, key: str | None = None) -> Dict[str, Any]:
    endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{AZURE_CONTENT_SAFETY_HOST.format(endpoint=endpoint)}/contentsafety/text:analyze?api-version=2023-10-01"
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("categoriesAnalysis", [])
    unsafe = any(item.get("severity", 0) >= 3 for item in scores)
    return {"service": "Azure AI Content Safety", "unsafe": unsafe, "raw": data}
