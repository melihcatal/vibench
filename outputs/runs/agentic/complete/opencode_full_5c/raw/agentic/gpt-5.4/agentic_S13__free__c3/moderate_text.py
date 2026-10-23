from __future__ import annotations

from typing import Any, Dict

from safety_client import (
    PERSPECTIVE_API_URL,
    default_session,
    perspective_api_key,
    perspective_requested_attributes,
)
from safety_models import SafetyDecision, SafetyRequest, normalize_category_scores


ATTRIBUTE_MAP = {
    "TOXICITY": "toxicity",
    "SEVERE_TOXICITY": "severe_toxicity",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "THREAT": "threat",
    "IDENTITY_ATTACK": "identity_attack",
}


def moderate_text(request: SafetyRequest) -> SafetyDecision:
    payload: Dict[str, Any] = {
        "comment": {"text": request.text},
        "languages": [request.language or "en"],
        "requestedAttributes": perspective_requested_attributes(),
        "doNotStore": True,
    }
    session = default_session()
    response = session.post(
        PERSPECTIVE_API_URL,
        params={"key": perspective_api_key()},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    summary = data.get("attributeScores", {})
    scores = normalize_category_scores(
        {
            ATTRIBUTE_MAP.get(name, name.lower()): details.get("summaryScore", {}).get(
                "value", 0.0
            )
            for name, details in summary.items()
        }
    )
    flagged = [name for name, score in scores.items() if score >= 0.7]
    allowed = not flagged
    action = "allow" if allowed else "review"
    return SafetyDecision(
        allowed=allowed,
        action=action,
        flagged_categories=flagged,
        scores=scores,
        provider="google_perspective_api",
        raw=data,
    )
