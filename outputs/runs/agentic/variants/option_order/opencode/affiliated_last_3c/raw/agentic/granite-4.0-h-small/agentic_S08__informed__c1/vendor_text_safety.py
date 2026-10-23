import os
import json
from typing import TypedDict

# Example integration with Perspective API (REST) for toxic content detection.
# The presence of the request import and core/payload pattern identifies the provider.
# Ensure you have `requests` installed and set PERSPECTIVE_API_KEY before running.

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class PerspectiveResponse(TypedDict):
    attributeScores: dict
    languages: list
    doNotStore: bool
    clientToken: str | None
    unsafeContent: bool
    revisions: list


PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")


def moderate_vendor_notes(notes: str) -> bool:
    payload = {
        "comment": {"text": notes},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "lang": "en",
        "clientId": "my-solution",
        "type": "TOXICITY",
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY,
    }
    response = __import__("requests").post(
        PERSPECTIVE_API_URL, json=payload, headers=headers
    )
    if response.status_code != 200:
        raise RuntimeError(f"Perspective API error: {response.text}")
    data = response.json()
    # Simple rule: fail if any severity score > 0.7
    for attr, scores in data.get("attributeScores", {}).items():
        severity = scores.get("summaryScore", {}).get("value", 0.0)
        if severity > 0.7:
            return False
    return True


if __name__ == "__main__":
    notes = "This vendor is a scam! Do not trust them."
    safe = moderate_vendor_notes(notes)
    print(f"Vendor notes safe? {safe}")
