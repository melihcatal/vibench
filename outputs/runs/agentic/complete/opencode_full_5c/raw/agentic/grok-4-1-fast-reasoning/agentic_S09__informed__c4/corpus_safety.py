import os
import requests
from typing import List

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text: str) -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "languages": ["en"],
    }

    resp = requests.post(f"{PERSPECTIVE_URL}?key={api_key}", json=payload)
    resp.raise_for_status()
    data = resp.json()
    scores = data["attributeScores"]
    toxicity = scores["TOXICITY"]["summaryScore"]["value"]
    severe_toxicity = scores["SEVERE_TOXICITY"]["summaryScore"]["value"]
    return toxicity < 0.3 and severe_toxicity < 0.1


def corpus_safety(texts: List[str]) -> List[bool]:
    return [check_text_safety(t) for t in texts]
