from __future__ import annotations

import os

import requests

from identity_models import ModerationResult

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"


def moderate_claim_text(text: str) -> ModerationResult:
    endpoint = os.environ[AZURE_CONTENT_SAFETY_ENDPOINT_ENV].rstrip("/")
    key = os.environ[AZURE_CONTENT_SAFETY_KEY_ENV]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    body = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    resp = requests.post(url, json=body, headers={"Ocp-Apim-Subscription-Key": key}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    categories = {item["category"]: float(item.get("severity", 0)) for item in data.get("categoriesAnalysis", [])}
    flagged = any(score >= 2 for score in categories.values())
    return ModerationResult(flagged=flagged, score=max(categories.values(), default=0.0), categories=categories, raw=data)
