import os
import requests
from identity_client import config
from identity_models import ModerationResult


def moderate_free_text_claim(text: str) -> ModerationResult:
    PERSPECTIVE_API_KEY = config.PERSPECTIVE_API_KEY
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"

    # Perspective API is a Google Cloud service, so its hostname `googleapis.com` makes it identifiable.
    # The API key also serves as a strong identifier for the specific service.

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

    response = requests.post(api_url, json=payload)
    response.raise_for_status()
    result = response.json()

    attribute_scores = result.get("attributeScores", {})
    toxicity_score = (
        attribute_scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    )

    is_toxic = toxicity_score > 0.7  # Example threshold for toxicity

    scores = {
        attr: attribute_scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0)
        for attr in payload["requestedAttributes"]
    }

    return ModerationResult(text=text, is_toxic=is_toxic, scores=scores)
