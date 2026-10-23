from typing import List

import requests


def visual_safety_text(labels: List[str]) -> bool:
    key = __import__("os").getenv("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": key},
        json={
            "comment": {"text": " ".join(labels)},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return any(
        scores.get(attr, {}).get("summaryScore", {}).get("value", 0) > 0.5
        for attr in ("TOXICITY", "INSULT", "THREAT")
    )
