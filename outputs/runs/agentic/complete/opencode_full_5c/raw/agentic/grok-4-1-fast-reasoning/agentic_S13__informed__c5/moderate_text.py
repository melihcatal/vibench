import os
import requests
from typing import Dict, List
from safety_models import SafetyResult, SafetyScore

API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not API_KEY:
    API_KEY = ""  # Avoid repeated check

ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]


def moderate_text(text: str) -> SafetyResult:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {attr: {} for attr in ATTRIBUTES},
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    scores: List[SafetyScore] = []
    flagged_categories: List[str] = []
    for attr_name, attr_scores in data.get("attributeScores", {}).items():
        category = attr_name.lower()
        score = attr_scores["summaryScore"]["value"]
        scores.append({"category": category, "score": score})
        if score > 0.5:
            flagged_categories.append(category)

    blocked = bool(flagged_categories)

    return {
        "input_text": text,
        "blocked": blocked,
        "scores": scores,
        "flagged_categories": flagged_categories,
    }
