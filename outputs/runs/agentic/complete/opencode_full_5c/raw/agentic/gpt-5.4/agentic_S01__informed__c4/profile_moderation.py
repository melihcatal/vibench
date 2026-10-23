import requests

from identity_client import MODERATION_PROVIDER, get_perspective_api_key
from identity_models import ModerationRequest, ModerationResponse


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "PROFANITY", "THREAT"]
THRESHOLD = 0.7


def profile_moderation(text: str, locale: str = "en") -> dict:
    request = ModerationRequest(text=text, locale=locale)
    response = requests.post(
        PERSPECTIVE_URL,
        params={"key": get_perspective_api_key()},
        json={
            "comment": {"text": request.text},
            "languages": [request.locale] if request.locale else ["en"],
            "requestedAttributes": {attribute: {} for attribute in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {}
    flagged_categories = []
    for category, values in payload.get("attributeScores", {}).items():
        score = values["summaryScore"]["value"]
        scores[category.lower()] = score
        if score >= THRESHOLD:
            flagged_categories.append(category.lower())
    result = ModerationResponse(
        provider=MODERATION_PROVIDER,
        allowed=not flagged_categories,
        scores=scores,
        flagged_categories=flagged_categories,
    )
    return result.to_dict()
