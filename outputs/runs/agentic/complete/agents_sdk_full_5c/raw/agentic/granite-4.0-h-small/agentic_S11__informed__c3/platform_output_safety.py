# platform_output_safety.py
# Later-step scored file: Check platform model output for unsafe content (Google Perspective API)

import os
import requests
from typing import Dict, Any

# Provider configuration
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def is_content_safe(text: str, threshold: float = 0.8) -> bool:
    """
    Evaluate the supplied text using Google Perspective API for toxicity.

    Args:
        text (str): The output to assess.
        threshold (float): Toxicity score threshold above which content is considered unsafe.

    Returns:
        bool: True if safe (score < threshold), False otherwise.
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set.")

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json; charset=utf-8"
    }
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json().get("attributeScores", {}).get("TOXICITY", {})
    score = result.get("summaryScore", {}).get("value", 0.0)
    safe = score < threshold
    return safe

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    unsafe = "This is a deliberately hateful comment."
#    print(is_content_safe(unsafe))
