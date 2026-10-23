import os
import requests
from messaging_models import PublishRequest

MODERATION_ENDPOINT = os.getenv(
    "PERSPECTIVE_API_ENDPOINT",
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
)
MODERATION_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_message_safety(request: PublishRequest) -> bool:
    """Detect unsafe content in a message payload using Perspective API."""
    if not MODERATION_ENDPOINT or not MODERATION_KEY:
        print("Perspective API credentials not configured, skipping safety check.")
        return True
    payload = {
        "comment": {"text": request["event_data"].get("text", "")},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(
        MODERATION_ENDPOINT,
        json=payload,
        headers={"x-api-key": MODERATION_KEY},
    )
    if response.status_code != 200:
        print(f"Safety check failed: {response.text}")
        return False
    result = response.json()
    toxicity = (
        result.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    )
    severity = (
        result.get("attributeScores", {})
        .get("SEVERE_TOXICITY", {})
        .get("summaryScore", {})
    )
    if toxicity.get("value", 0) > 0.7 or severity.get("value", 0) > 0.7:
        print("Unsafe content detected, publish aborted.")
        return False
    return True
