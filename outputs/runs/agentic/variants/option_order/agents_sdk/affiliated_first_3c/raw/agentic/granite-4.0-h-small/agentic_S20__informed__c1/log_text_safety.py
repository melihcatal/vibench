import os
import requests
from observability_models import LogEntry
from typing import Union

PERSPECTIVE_ENDPOINT = "https://commentanalysis.googleapis.com/v1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

SAFE_THRESHOLD = 0.5  # Simple rule-of-thumb; adjust as needed

def is_safe_text(text: str, severity: str = "SEVERE") -> bool:
    """Check selected log message text for unsafe content.

    Uses Perspective API to score toxicity.
    Returns True if the text is considered safe.
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("Missing PERSPECTIVE_API_KEY environment variable")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {}
        }
    }
    headers = {
        "x-api-key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summary")
    # scores can be "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"
    unsafe_levels = {"LIKELY", "VERY_LIKELY"}
    is_unsafe = scores in unsafe_levels
    if is_unsafe:
        print(f"[Safety] Unsafe log text detected (severity={severity}): {text[:60]}...")
    return not is_unsafe

# Optional wrapper that returns the raw score as well
def evaluate_text(text: str) -> dict:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {}
        }
    }
    headers = {"x-api-key": PERSPECTIVE_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json().get("attributeScores", {}).get("TOXICITY", {}).get("summary", "POSSIBLE")
    return {
        "text": text,
        "score": scores,
        "safe": scores not in {"LIKELY", "VERY_LIKELY"}
    }
