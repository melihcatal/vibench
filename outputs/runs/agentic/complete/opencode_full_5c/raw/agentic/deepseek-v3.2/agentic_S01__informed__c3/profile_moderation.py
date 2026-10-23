import os
import requests


def profile_moderation(text: str) -> dict:
    """Moderate profile text before account activation using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
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

    params = {"key": api_key}

    try:
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()
        data = response.json()

        scores = {}
        for attribute_name, attribute_data in data.get("attributeScores", {}).items():
            scores[attribute_name.lower()] = attribute_data.get("summaryScore", {}).get(
                "value", 0
            )

        return {
            "text": text,
            "scores": scores,
            "is_acceptable": all(score < 0.7 for score in scores.values()),
            "highest_risk": max(scores.items(), key=lambda x: x[1])
            if scores
            else ("none", 0),
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to moderate text with Perspective API: {str(e)}")
