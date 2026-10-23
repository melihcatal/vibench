from __future__ import annotations

from security_client import perspective_session, perspective_url
from security_models import PayloadSafetyResult


def payload_safety(text: str) -> PayloadSafetyResult:
    session = perspective_session()
    response = session.post(
        perspective_url(),
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): data["summaryScore"]["value"]
        for name, data in payload.get("attributeScores", {}).items()
    }
    flagged = [name for name, score in scores.items() if score >= 0.7]
    return PayloadSafetyResult(
        provider="google-perspective-api",
        safe=not flagged,
        scores=scores,
        flagged_categories=flagged,
    )
