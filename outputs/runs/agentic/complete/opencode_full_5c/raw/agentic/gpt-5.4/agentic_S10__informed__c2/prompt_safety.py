import os

import requests

from model_models import SafetyResult, normalize_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str, threshold: float = 0.7) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    result = SafetyResult(
        provider="Perspective API",
        flagged=any(score >= threshold for score in scores.values()),
        scores=scores,
        details=data,
    )
    return {
        "provider": result.provider,
        "flagged": result.flagged,
        "scores": result.scores,
        "details": result.details,
    }
