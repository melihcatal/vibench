import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_prompt_safety(text: str, threshold: float = 0.8) -> dict:
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    value = float(scores.get("value", 0.0))
    return {"unsafe": value >= threshold, "score": value, "raw": response.json()}
