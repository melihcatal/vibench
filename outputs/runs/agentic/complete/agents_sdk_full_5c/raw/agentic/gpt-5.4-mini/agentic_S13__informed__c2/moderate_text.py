from __future__ import annotations

from safety_client import SafetyClient
from safety_models import TextSafetyRequest


client = SafetyClient()


def moderate_text(text: str) -> dict:
    request = TextSafetyRequest(text=text, categories=["Hate", "SelfHarm", "Sexual", "Violence"])
    decision = client.analyze_text(request)
    return {
        "allowed": decision.allowed,
        "scores": decision.scores,
        "labels": decision.labels,
        "provider": decision.provider,
    }
