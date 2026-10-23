import os
from typing import Dict, Any, Optional
from safety_client import post_to_api
from safety_models import SafetyResult


def apply_safety_threshold(
    text: str, thresholds: Optional[Dict[str, float]] = None
) -> SafetyResult:
    if thresholds is None:
        thresholds = {
            "toxicity": 0.7,
            "severe_toxicity": 0.4,
            "insult": 0.7,
            "threat": 0.7,
        }
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    attrs = {k.upper(): {} for k in thresholds}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": attrs,
    }
    data = post_to_api(url, payload, api_key, key_is_query=True)
    categories: Dict[str, float] = {}
    blocked_reasons = []
    for attr, score_obj in data.get("attributeScores", {}).items():
        score = score_obj["summaryScore"].get("mean", 0.0)
        cat_lower = attr.lower()
        categories[cat_lower] = score
        if thresholds.get(cat_lower, 0.0) < score:
            blocked_reasons.append(attr)
    overall_blocked = bool(blocked_reasons)
    rationale = (
        f"Exceeded thresholds for: {', '.join(blocked_reasons)}"
        if blocked_reasons
        else "All scores below thresholds"
    )
    return {
        "categories": categories,
        "overall_blocked": overall_blocked,
        "rationale": rationale,
        "redacted_text": "",
        "flagged_spans": [],
        "raw_response": data,
    }
