import requests

# Provider: Perspective API for prompt and output safety checks

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def is_safe(text: str) -> bool:
    """Return True if the text passes the safety moderation filter."""
    if not PERSPECTIVE_API_KEY:
        raise ValueError("Set PERSPECTIVE_API_KEY environment variable")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    # Require both TOXICITY and SEVERE_TOXICITY to be below a threshold
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    severe = scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return toxicity < 0.5 and severe < 0.5
