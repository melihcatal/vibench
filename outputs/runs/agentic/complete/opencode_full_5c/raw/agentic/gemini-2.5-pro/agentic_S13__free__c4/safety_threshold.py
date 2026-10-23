from typing import Dict
from safety_client import get_perspective_client
from safety_models import SafetyThresholdDecision

DEFAULT_THRESHOLDS = {
    "TOXICITY": 0.8,
    "SEVERE_TOXICITY": 0.6,
    "IDENTITY_ATTACK": 0.7,
    "INSULT": 0.75,
    "PROFANITY": 0.8,
    "THREAT": 0.5,
}


def apply_safety_thresholds(
    text: str, thresholds: Dict[str, float] = None
) -> SafetyThresholdDecision:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    client = get_perspective_client()
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in thresholds.keys()},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    is_allowed = True
    flagged_categories = {}

    for attr, value in response["attributeScores"].items():
        score = value["summaryScore"]["value"]
        if score > thresholds.get(attr, 1.0):
            is_allowed = False
            flagged_categories[attr] = score

    return SafetyThresholdDecision(
        text=text, is_allowed=is_allowed, flagged_categories=flagged_categories
    )
