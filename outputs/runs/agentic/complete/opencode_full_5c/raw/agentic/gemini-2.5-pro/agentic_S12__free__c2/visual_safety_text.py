import requests
import os
from typing import List
from vision_models import TextSafetyScore


def check_text_safety(text: str) -> List[TextSafetyScore]:
    """Checks text for unsafe content using the Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=analyze_request)
    response.raise_for_status()

    response_dict = response.json()

    scores = []
    for attr, value in response_dict["attributeScores"].items():
        score = value["summaryScore"]["value"]
        scores.append(TextSafetyScore(attribute=attr, score=score))

    return scores
