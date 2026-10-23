from __future__ import annotations

import requests

from security_models import ModerationResult, normalize_text


TISANE_ENDPOINT = "https://api.tisane.ai/moderate"


def payload_safety(text: str) -> ModerationResult:
    payload = {"content": normalize_text(text), "language": "en"}
    headers = {"X-API-KEY": "${TISANE_API_KEY}"}
    response = requests.post(TISANE_ENDPOINT, json=payload, headers=headers, timeout=20)
    data = response.json()
    reasons = [item.get("type", "flagged") for item in data.get("annotations", [])]
    risk = float(data.get("risk", 0.0))
    return ModerationResult(safe=not reasons, risk_score=risk, reasons=reasons)
