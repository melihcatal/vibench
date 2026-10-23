from __future__ import annotations

import os
from typing import Dict

import requests

from document_models import SafetyResult


def check_document_safety(text: str) -> SafetyResult:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    payload: Dict[str, object] = {"text": text}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    categories = {item.get("categoryName", ""): item for item in data.get("categoriesAnalysis", [])}
    unsafe = any((item.get("severity", 0) or 0) >= 2 for item in data.get("categoriesAnalysis", []))
    return SafetyResult(unsafe=unsafe, categories=categories, raw=data)
