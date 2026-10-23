from __future__ import annotations

import requests

from translation_client import PERSPECTIVE_ANALYZE_ENDPOINT, perspective_params


def unsafe_copy_check(text: str, language: str) -> dict[str, float | bool]:
    response = requests.post(
        PERSPECTIVE_ANALYZE_ENDPOINT,
        params=perspective_params(),
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    scores = response.json()["attributeScores"]
    toxicity = scores["TOXICITY"]["summaryScore"]["value"]
    insult = scores["INSULT"]["summaryScore"]["value"]
    threat = scores["THREAT"]["summaryScore"]["value"]
    sexual = scores["SEXUALLY_EXPLICIT"]["summaryScore"]["value"]
    return {
        "unsafe": max(toxicity, insult, threat, sexual) >= 0.7,
        "toxicity": toxicity,
        "insult": insult,
        "threat": threat,
        "sexually_explicit": sexual,
    }
