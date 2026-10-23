import os
import requests
from typing import List, Dict

API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text_labels: List[str]) -> Dict[str, Dict]:
    """
    Checks a list of text labels for toxicity using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    results = {}
    for label in text_labels:
        params = {"key": api_key}
        data = {
            "comment": {"text": label},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }

        response = requests.post(API_URL, params=params, json=data)
        response.raise_for_status()

        resp_data = response.json()
        toxicity_score = resp_data["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        results[label] = {"toxicity_score": toxicity_score}

    return results
