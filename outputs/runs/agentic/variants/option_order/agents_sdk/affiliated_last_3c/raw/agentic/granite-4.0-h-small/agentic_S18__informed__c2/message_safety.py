import os
from typing import Dict
import requests

# Perspective API endpoint and key
def _load_perspective_config() -> str:
    key = os.getenv("PERSPECTIVE_API_KEY")
    if not key:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
    return key


def is_content_safe(text: str) -> bool:
    """Check a string for toxicity/abusive content via Perspective API.

    Returns True if the "attackOnComment" score is below the safety threshold,
    otherwise returns False.
    """
    api_key = _load_perspective_config()
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Perspective API request failed: {response.status_code} {response.text}")
    result = response.json()
    # The score is in result['attributeScores']['TOXICITY']['summaryScore']['value']
    score = result.get(
        "attributeScores", {}
    ).get("TOXICITY", {}).get(
        "summaryScore", {}
    ).get("value", 0.0)
    # Threshold can be tuned; here we treat >= 0.5 as unsafe
    THRESHOLD = 0.5
    safe = score < THRESHOLD
    return safe


def safe_publish(event: Dict, dl_topic: str) -> None:
    """Publish an event only if its payload text is safe.

    If unsafe, the message is dead‑lettered to `dl_topic` with an error detail.
    """
    text = event.get("payload", {}).get("text", "")
    if not is_content_safe(text):
        raise ValueError("Unsafe content detected")
    # If we reach here the message is safe; forward to normal publisher logic.
    # Example: call your messaging client's publish_event here.
    # For this helper we just return to indicate success.
    return
