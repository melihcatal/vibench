from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyCheckResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2023-10-01"


def check_platform_output_safety(text: str) -> SafetyCheckResult:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise RuntimeError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={API_VERSION}"
    payload: Dict[str, Any] = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    headers = {"Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    severities = data.get("categoriesAnalysis", [])
    is_safe = all(item.get("severity", 0) < 3 for item in severities)
    return SafetyCheckResult(is_safe=is_safe, provider="azure-ai-content-safety", categories={"analysis": severities}, raw=data)
