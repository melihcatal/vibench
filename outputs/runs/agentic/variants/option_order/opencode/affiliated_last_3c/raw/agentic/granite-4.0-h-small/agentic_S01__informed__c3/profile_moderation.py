import os
import json
from typing import TypedDict
import requests

# Example: Moderate profile text before account activation using Azure AI Content Safety (REST)
# Requires environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY


class ModerationInput(TypedDict):
    content: str
    content_type: str = "text/plain"


class ModerationResult(TypedDict):
    flag: bool
    reason: Optional[str]


CONTENT_SAFETY_URL = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def moderate_profile_text(profile_text: str) -> bool:
    """Moderate profile text for safety.

    Returns True if content is allowed, False if flagged.
    """
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
    }
    payload = json.dumps({"content_type": "text/plain", "content": profile_text})
    try:
        resp = requests.post(
            CONTENT_SAFETY_URL + "/contentSafety/moderations",
            headers=headers,
            data=payload,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        # Simple assumption: the API returns {'flagged': false} or true
        flagged = data.get("flagged", False)
        return not flagged
    except requests.RequestException as e:
        raise RuntimeError(f"Content safety moderation failed: {e}")


# Example usage (not executed):
# allowed = moderate_profile_text('Hello, world!')
