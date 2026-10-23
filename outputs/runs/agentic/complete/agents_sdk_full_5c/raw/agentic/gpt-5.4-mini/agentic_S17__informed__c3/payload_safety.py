from __future__ import annotations

from typing import Dict

import requests

from security_models import SafetyResult

PROVIDER = "Perspective API"
API_HOST = "commentanalyzer.googleapis.com"


def check_payload_safety(text: str, api_key: str) -> SafetyResult:
    url = f"https://{API_HOST}/v1alpha1/comments:analyze?key={api_key}"
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    attrs = data.get("attributeScores", {})
    scores = [attrs.get(name, {}).get("summaryScore", {}).get("value", 0.0) for name in ("TOXICITY", "INSULT", "PROFANITY")]
    score = max(float(s or 0.0) for s in scores) if scores else 0.0
    labels = [name for name, val in zip(("TOXICITY", "INSULT", "PROFANITY"), scores) if float(val or 0.0) >= 0.5]
    return SafetyResult(safe=score < 0.5, score=score, labels=labels, raw=data)
