import os
import requests
import json
from typing import Dict, Any


def check_prompt_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=data)
    response.raise_for_status()

    result = response.json()

    scores = {}
    if "attributeScores" in result:
        for attr_name, attr_data in result["attributeScores"].items():
            scores[attr_name] = attr_data["summaryScore"]["value"]

    is_safe = all(score < 0.7 for score in scores.values()) if scores else True

    return {"is_safe": is_safe, "scores": scores, "text": text}
