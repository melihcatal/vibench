"""
Apply category thresholds to decide whether to allow text using Azure AI Content Safety.
"""
from typing import Dict
from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, SafetyCategory


def apply_safety_threshold(
    text: str, thresholds: Dict[SafetyCategory, float]
) -> dict:
    """Apply category thresholds to decide whether to allow text."""
    client = AzureContentSafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)

    custom_decisions = []
    for decision in response.decisions:
        threshold = thresholds.get(decision["category"], decision["threshold"])
        custom_decisions.append({
            **decision,
            "flagged": decision["score"] >= threshold,
            "threshold": threshold,
        })

    return {
        "text": text,
        "allowed": not any(d["flagged"] for d in custom_decisions),
        "decisions": [
            {
                "category": decision["category"].value,
                "score": decision["score"],
                "flagged": decision["flagged"],
                "threshold": decision["threshold"],
            }
            for decision in custom_decisions
        ],
    }