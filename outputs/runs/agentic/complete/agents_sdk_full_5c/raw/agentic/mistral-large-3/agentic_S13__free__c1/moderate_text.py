# Scores user text for unsafe or policy-violating content
from typing import Dict
from google.cloud import language_v1
from safety_models import SafetyCategory, SafetyDecision, normalize_scores
from safety_client import get_perspective_client


def moderate_text(text: str) -> SafetyDecision:
    """Score text using Google Perspective API."""
    client = get_perspective_client()
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {}
    }

    response = client.analyze_comment(
        request={
            "comment": {"text": text},
            "requested_attributes": requested_attributes,
            "language_code": "en"
        }
    )

    scores = {}
    for attr, value in response.attribute_scores.items():
        scores[attr.lower()] = value.summary_score.value

    normalized_scores = normalize_scores(scores)
    thresholds = {
        SafetyCategory.HATE: 0.7,
        SafetyCategory.VIOLENCE: 0.8,
        SafetyCategory.SEXUAL: 0.6,
        SafetyCategory.SELF_HARM: 0.9,
        SafetyCategory.HARASSMENT: 0.7,
        SafetyCategory.DANGEROUS: 0.8
    }

    blocked_reason = None
    for category, score in normalized_scores.items():
        if score >= thresholds[category]:
            blocked_reason = f"high {category.value} score"
            break

    decision = SafetyDecision(
        allowed=blocked_reason is None,
        categories=normalized_scores,
        blocked_reason=blocked_reason
    )
    return decision