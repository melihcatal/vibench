from __future__ import annotations

import os

import requests

from speech_models import SafetyAssessment, normalize_transcript_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def check_live_caption_safety(text: str, threshold: float = 0.8) -> SafetyAssessment:
    cleaned = normalize_transcript_text(text)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": cleaned},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()["attributeScores"]
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.items()
    }
    flagged = [name for name, score in scores.items() if score >= threshold]
    return SafetyAssessment(is_safe=not flagged, scores=scores, flagged_categories=flagged)
