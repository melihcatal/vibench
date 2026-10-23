from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyReport

PROVIDER = "azure-ai-content-safety"
ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.contentsafety.azure.com")
API_VERSION = "2024-09-01"


def check_text(text: str) -> SafetyReport:
    url = f"{ENDPOINT.rstrip('/')}/contentsafety/text:analyze?api-version={API_VERSION}"
    headers = {"Ocp-Apim-Subscription-Key": os.getenv("AZURE_CONTENT_SAFETY_KEY", "")}
    payload: Dict[str, Any] = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    raw = response.json()
    categories = [item.get("category", "") for item in raw.get("categoriesAnalysis", []) if item.get("severity", 0) > 0]
    return SafetyReport(flagged=bool(categories), categories=categories, raw=raw)
