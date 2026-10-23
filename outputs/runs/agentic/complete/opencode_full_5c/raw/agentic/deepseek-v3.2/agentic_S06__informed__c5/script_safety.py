import os
import requests
from typing import Dict, List, Any, Optional


def check_content_safety(text: str) -> Dict[str, Any]:
    """
    Check narration scripts for unsafe content using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
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

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()

        result = response.json()

        scores = {}
        attribute_scores = result.get("attributeScores", {})

        for attribute, score_data in attribute_scores.items():
            scores[attribute] = score_data.get("summaryScore", {}).get("value", 0.0)

        is_safe = all(score < 0.7 for score in scores.values())

        return {
            "is_safe": is_safe,
            "scores": scores,
            "flagged_attributes": [
                attr for attr, score in scores.items() if score >= 0.7
            ],
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Content safety check failed: {str(e)}")


def check_batch_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Check multiple narration scripts for unsafe content.
    """
    results = []

    for text in texts:
        try:
            result = check_content_safety(text)
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "is_safe": False,
                    "error": str(e),
                    "scores": {},
                    "flagged_attributes": [],
                }
            )

    return results
