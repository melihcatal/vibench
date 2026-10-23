import os
import requests
from .speech_models import ModerationRequest, ModerationResponse


def moderate_transcript(text: str) -> ModerationResponse:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
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

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    categories = {}
    scores = {}
    for attribute in data["attributeScores"]:
        categories[attribute] = (
            data["attributeScores"][attribute]["summaryScore"]["value"] > 0.7
        )
        scores[attribute] = data["attributeScores"][attribute]["summaryScore"]["value"]

    return ModerationResponse(
        flagged=any(categories.values()), categories=categories, scores=scores
    )
