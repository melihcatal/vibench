import os
from typing import Any, Dict
import requests
from messaging_models import parse_response

# Provider: Perspective API (example) for toxicity detection
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": PERSPECTIVE_API_KEY,
}

safety_categories = {
    "TOXICITY": "unsafe",
    # Add other categories as needed
}


def check_safety(payload_text: str, category: str = "TOXICITY") -> Dict[str, Any]:
    """Send payload text to Perspective API and return safety assessment.
    Returns a dict with fields like `attributeScores` containing the score.
    """
    data = {
        "comment": {"text": payload_text},
        "requestedAttributes": {category: {}},
    }
    resp = requests.post(PERSPECTIVE_API_URL, headers=HEADERS, json=data)
    resp.raise_for_status()
    result = parse_response(resp.content)
    # Normalize the response to a simple flag + score
    score = result.get("attributeScores", {}).get(category, {}).get("summaryScore", {})
    is_unsafe = score.get("value", 0.0) > 0.5  # threshold example
    return {
        "category": category,
        "score": score.get("value", 0.0),
        "unsafe": is_unsafe,
        "details": result,
    }


if __name__ == "__main__":
    # Demo: evaluate a sample message
    sample = "This is a test comment that might be toxic."
    assessment = check_safety(sample)
    print("Safety assessment:", assessment)
