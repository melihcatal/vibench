from typing import Dict
from safety_client import get_perspective_client


def moderate_text(text: str) -> Dict[str, float]:
    """
    Analyzes a text for toxic content using the Perspective API.
    """
    client = get_perspective_client()

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

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, value in response["attributeScores"].items():
        scores[attribute] = value["summaryScore"]["value"]

    return scores
