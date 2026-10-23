import os
import requests


def record_text_safety(text: str) -> bool:
    endpoint = os.getenv("PERSPECTIVE_API_KEY")
    if not endpoint:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": endpoint},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score < 0.7
