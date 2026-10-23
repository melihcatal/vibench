from __future__ import annotations

from typing import Any, Dict

from safety_client import PERSPECTIVE_API_BASE, SafetyClientConfig, SafetyHTTPClient
from safety_models import SafetyDecision, SafetyRequest, normalize_scores


def moderate_text(text: str, language: str | None = None) -> SafetyDecision:
    request = SafetyRequest(text=text, language=language)
    config = SafetyClientConfig.from_env("perspective")
    client = SafetyHTTPClient(config)
    payload: Dict[str, Any] = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}, "PROFANITY": {}},
        "doNotStore": True,
    }
    if request.language:
        payload["languages"] = [request.language]
    data = client.post(PERSPECTIVE_API_BASE, json=payload, headers=client.perspective_headers())
    attrs = data.get("attributeScores", {})
    scores = {name.lower(): info.get("summaryScore", {}).get("value", 0.0) for name, info in attrs.items()}
    scores = normalize_scores(scores)
    best = max(scores.items(), key=lambda kv: kv[1], default=("allow", 0.0))
    label = "unsafe" if best[1] >= 0.5 else "allow"
    return SafetyDecision(label=label, score=best[1], categories=scores, raw=data)
