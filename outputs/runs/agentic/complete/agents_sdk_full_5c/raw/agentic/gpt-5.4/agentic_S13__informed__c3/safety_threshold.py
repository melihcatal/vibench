from __future__ import annotations

from typing import Dict

from safety_client import analyze_text, get_azure_content_safety_config
from safety_models import normalize_azure_categories


DEFAULT_THRESHOLDS = {
    "hate": 2,
    "selfharm": 1,
    "sexual": 3,
    "violence": 2,
}


def decide_text_allowance(text: str, thresholds: Dict[str, float] | None = None) -> dict:
    active_thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    response_json = analyze_text(text)
    categories = normalize_azure_categories(response_json)
    decisions = []
    allow = True
    for category in categories:
        threshold = float(active_thresholds.get(category.name, 4))
        exceeded = category.score >= threshold
        decisions.append(
            {
                "category": category.name,
                "score": category.score,
                "threshold": threshold,
                "exceeded": exceeded,
            }
        )
        if exceeded:
            allow = False
    return {
        "provider": get_azure_content_safety_config()["provider"],
        "model": "Azure AI Content Safety text:analyze",
        "allow": allow,
        "decisions": decisions,
        "raw_response": response_json,
    }
