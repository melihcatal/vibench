from __future__ import annotations

import os
from typing import List

import requests

from security_models import SafetyCheckResult, normalize_label_text

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def secret_label_safety(label: str, note: str = "") -> SafetyCheckResult:
    cleaned = normalize_label_text(f"{label} {note}")
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    reasons: List[str] = []
    if not cleaned:
        reasons.append("empty label")
    if any(term in cleaned.lower() for term in ["password", "token", "secret", "ssn"]):
        reasons.append("sensitive wording")

    if api_key:
        payload = {
            "comment": {"text": cleaned},
            "requestedAttributes": {"TOXICITY": {}},
            "doNotStore": True,
            "languages": ["en"],
        }
        response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=10)
        if response.ok:
            toxicity = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
            if toxicity >= 0.5:
                reasons.append("perspective flagged text")
    return SafetyCheckResult(label=label, safe=not reasons, reasons=reasons)
