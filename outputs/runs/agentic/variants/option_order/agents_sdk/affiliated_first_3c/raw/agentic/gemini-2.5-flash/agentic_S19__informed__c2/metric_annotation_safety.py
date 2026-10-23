import os
import requests
from typing import Dict, Any

def check_annotation_safety(text: str, threshold: float = 0.7) -> Dict[str, Any]:
    """
    Checks free-text metric labels or annotations for unsafe text using Perspective API.
    Returns a dictionary of safety scores.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"] # Specify language for analysis
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        safety_scores = {}
        for attribute, details in result.get("attributeScores", {}).items():
            score = details.get("summaryScore", {}).get("value")
            if score is not None:
                safety_scores[attribute] = score
        return safety_scores

    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
