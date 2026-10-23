from __future__ import annotations

import requests

from document_client import get_perspective_api_key, get_perspective_endpoint


def check_ocr_text_safety(text: str, languages: list[str] | None = None) -> dict:
    response = requests.post(
        get_perspective_endpoint(),
        params={"key": get_perspective_api_key()},
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
            "languages": languages or ["en"],
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in payload.get("attributeScores", {}).items()
    }
    max_score = max(scores.values(), default=0.0)
    return {
        "provider": "commentanalyzer.googleapis.com",
        "is_unsafe": max_score >= 0.7,
        "scores": scores,
        "raw": payload,
    }
