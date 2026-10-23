"""Check platform model output for unsafe content using Azure AI Content Safety.

Provider: Azure AI Content Safety via REST.
Environment: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY.
"""

from __future__ import annotations

import os
from typing import Dict

import requests

from model_models import SafetyResult


def check_platform_output_for_safety(text: str) -> SafetyResult:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data: Dict[str, object] = response.json()
    categories = data.get("categoriesAnalysis", {}) if isinstance(data, dict) else {}
    severity = float(data.get("sexual", {}).get("severity", 0)) if isinstance(data, dict) else 0.0
    flagged = any(int(item.get("severity", 0)) >= 4 for item in categories.values()) if isinstance(categories, dict) else False
    return SafetyResult(flagged=flagged, score=severity, categories=dict(categories))
