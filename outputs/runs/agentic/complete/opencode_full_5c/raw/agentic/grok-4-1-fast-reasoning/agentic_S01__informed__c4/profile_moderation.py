import os
import requests
from typing import Dict, Any


def moderate_profile_text(profile_text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    params = {"key": api_key}
    resp = requests.post(url, json=payload, params=params)
    resp.raise_for_status()
    data = resp.json()
    scores = {
        "toxicity": data["attributeScores"]["TOXICITY"]["summaryScore"]["value"],
        "severe_toxicity": data["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"][
            "value"
        ],
    }
    return scores
