from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_ocr_safety(text: str, languages: list[str] | None = None) -> dict:
    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {"provider": "perspective", "scores": scores, "raw": data}
