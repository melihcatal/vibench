from typing import List, Tuple

import requests

from safety_client import get_config
from safety_models import SafetyDecision, normalize_text


def redact_unsafe(text: str) -> SafetyDecision:
    cfg = get_config()
    url = (
        f"{cfg['endpoint']}/contentsafety/text:analyze?api-version={cfg['api_version']}"
    )
    payload = {"text": normalize_text(text), "outputType": "TextSpan"}
    resp = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": cfg["key"],
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    data = resp.json()
    redacted = data.get("redactedText") or data.get("text", normalize_text(text))
    return SafetyDecision(
        allowed=not data.get("blocklistMatched", False),
        scores=data.get("categoriesAnalysis", {}),
        labels=data.get("labels", []),
        redacted_text=redacted,
        raw=data,
    )
