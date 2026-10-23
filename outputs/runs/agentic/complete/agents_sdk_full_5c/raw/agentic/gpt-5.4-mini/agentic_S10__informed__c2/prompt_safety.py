import os
from model_models import SafetyResult
import requests

PERSPECTIVE_API_KEY = os.environ["PERSPECTIVE_API_KEY"]
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> SafetyResult:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    r = requests.post(
        f"{PERSPECTIVE_ENDPOINT}?key={PERSPECTIVE_API_KEY}",
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return SafetyResult(unsafe=score >= 0.7, score=score, raw=data)
