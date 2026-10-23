import requests
import os


def is_prompt_safe(text: str) -> bool:
    """Check text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY not set")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_HATE": {},
        },
        "languages": ["en"],
        "clientId": "my-app",
    }
    headers = {"key": api_key}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    # Simple safety check: if any toxicity score exceeds 0.7, flag unsafe
    scores = result.get("attributeScores", {})
    for attr in ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_HATE"]:
        score = scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0)
        if score > 0.7:
            return False
    return True
