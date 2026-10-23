from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_safety(texts: list[str], threshold: float = 0.7) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    results = []
    flagged = []
    for index, text in enumerate(texts):
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}},
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        item = {
            "index": index,
            "text": text,
            "toxicity": score,
            "safe": score < threshold,
        }
        results.append(item)
        if score >= threshold:
            flagged.append(item)
    return {
        "provider": "Perspective API",
        "results": results,
        "flagged": flagged,
        "all_safe": not flagged,
    }
