from __future__ import annotations

import os
from typing import Optional

import requests

from model_models import SafetyResult

AZURE_CONTENT_SAFETY_ENDPOINT_VAR = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_VAR = "AZURE_CONTENT_SAFETY_KEY"


def check_safety(text: str) -> SafetyResult:
    endpoint = os.getenv(AZURE_CONTENT_SAFETY_ENDPOINT_VAR, "")
    key = os.getenv(AZURE_CONTENT_SAFETY_KEY_VAR, "")
    url = endpoint.rstrip("/") + "/contentsafety/text:analyze?api-version=2024-02-15-preview"
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    resp = requests.post(url, json=payload, headers={"Ocp-Apim-Subscription-Key": key})
    resp.raise_for_status()
    data = resp.json()
    category = None
    score: Optional[float] = None
    flagged = False
    for item in data.get("categoriesAnalysis", []):
        if item.get("severity", 0) > 1:
            flagged = True
            category = item.get("category")
            score = float(item.get("severity", 0))
            break
    return SafetyResult(flagged=flagged, category=category, score=score, raw=data)
