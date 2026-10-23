from __future__ import annotations

from security_client import perspective_session, require_env
from security_models import SafetyAssessment


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_payload_safety(text: str) -> SafetyAssessment:
    api_key = require_env("PERSPECTIVE_API_KEY")
    session = perspective_session()
    response = session.post(
        PERSPECTIVE_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: payload["summaryScore"]["value"]
        for name, payload in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    verdict = "unsafe" if flagged else "acceptable"
    return SafetyAssessment(provider="perspective-api", verdict=verdict, scores=scores, flagged=flagged)
