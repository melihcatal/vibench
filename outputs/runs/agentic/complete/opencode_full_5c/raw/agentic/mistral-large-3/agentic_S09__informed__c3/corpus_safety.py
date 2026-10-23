import os
import requests
from typing import List, Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Check corpus text for toxicity using Perspective API."""
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        params = {"key": PERSPECTIVE_API_KEY}
        response = requests.post(PERSPECTIVE_API_URL, json=payload, params=params)
        if response.status_code == 200:
            results.append(
                {
                    "text": text,
                    "toxicity_score": response.json()["attributeScores"]["TOXICITY"][
                        "summaryScore"
                    ]["value"],
                }
            )
        else:
            results.append({"text": text, "error": response.text})
    return results
