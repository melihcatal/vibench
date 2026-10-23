from __future__ import annotations

from typing import Dict

from safety_client import SafetyClient
from safety_models import TextSafetyRequest


client = SafetyClient()


def safety_threshold(text: str, thresholds: Dict[str, float]) -> dict:
    decision = client.analyze_text(TextSafetyRequest(text=text, categories=list(thresholds.keys())))
    allowed = True
    for category, threshold in thresholds.items():
        if decision.scores.get(category, 0.0) >= threshold:
            allowed = False
            break
    return {"allowed": allowed, "scores": decision.scores, "provider": decision.provider}
