import os
import requests
from speech_models import SafetyRating


def check_live_caption_safety(text: str) -> list[SafetyRating] | None:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
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
        response = requests.post(url, json=request_body)
        response.raise_for_status()
        data = response.json()

        scores = data.get("attributeScores", {})
        ratings = []
        for attribute, value in scores.items():
            ratings.append(
                SafetyRating(
                    attribute=attribute,
                    score=value.get("summaryScore", {}).get("value", 0.0),
                )
            )
        return ratings
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return None
