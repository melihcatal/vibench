import os
import requests

# Perspective API for content safety checks
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(text: str, attributes: list = ["TOXICITY", "SEXTENSION"]):
    """Checks the provided text for unsafe content using Perspective API.

    Args:
        text: The text to evaluate.
        attributes: List of attribute names to check (default TOXICITY, SEXPENSION).

    Returns:
        A dict with attribute scores (0.0‑1.0). Higher values indicate risk.
    """
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "clientToken": "",  # optional
    }
    headers = {
        "key": PERSPECTIVE_API_KEY,
        "content-type": "application/json",
    }
    resp = requests.post(API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["attributeScores"]
