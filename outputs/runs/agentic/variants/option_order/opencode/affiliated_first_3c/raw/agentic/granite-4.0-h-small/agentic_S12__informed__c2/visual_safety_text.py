# visual_safety_text.py
"""Later-step integration: Check generated visual labels for unsafe text.

Uses Perspective API (REST) to evaluate toxicity of any extracted text (labels or OCR).
"""

import requests
import json

# Provider identifiers (Perspective API)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1beta1/comments:analyze"


def is_text_safe(text: str) -> bool:
    """Determine whether a piece of text contains toxic or unsafe content.

    Args:
        text: The string to evaluate (e.g., a label or OCR result).

    Returns:
        True if the content is deemed safe, False otherwise.
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "clientId": "vibench-safety-check",
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PERSPECTIVE_API_KEY,
    }
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    # Perspective API returns a list of attribute scores; we focus on TOXICITY
    scores = result.get("attributeScores", {})
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {})
    score = toxicity.get("value", 0.0)
    # Threshold can be tuned; here we treat >=0.5 as unsafe
    return score < 0.5
