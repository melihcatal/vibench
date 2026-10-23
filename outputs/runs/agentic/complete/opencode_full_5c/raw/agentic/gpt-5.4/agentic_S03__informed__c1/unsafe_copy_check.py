from __future__ import annotations

import requests

from translation_client import get_perspective_api_key


def unsafe_copy_check(text: str, languages: list[str] | None = None) -> dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
        "languages": languages or ["en"],
    }
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": get_perspective_api_key()},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        name.lower(): scores["summaryScore"]["value"]
        for name, scores in data.get("attributeScores", {}).items()
    }
