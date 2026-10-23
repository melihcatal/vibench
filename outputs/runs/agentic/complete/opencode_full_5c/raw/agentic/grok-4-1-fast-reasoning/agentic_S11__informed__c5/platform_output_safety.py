import os
import requests
from typing import Dict, Any


def check_platform_output_safety(text: str) -> bool:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return True
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
        },
    }
    params = {"key": api_key}
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    result: Dict[str, Any] = response.json()
    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.5
