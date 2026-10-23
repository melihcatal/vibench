from __future__ import annotations

from vision_client import perspective_headers, perspective_url, post_json
from vision_models import TextSafetyResult


PROVIDER = "perspective-api"


def visual_safety_text(text: str, threshold: float = 0.7) -> TextSafetyResult:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    data = post_json(perspective_url(), payload, headers=perspective_headers())
    scores = {
        key: value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    return TextSafetyResult(provider=PROVIDER, scores=scores, flagged=flagged)
