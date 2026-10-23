import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def redact_unsafe(text: str, min_unsafe_score: float = 0.5) -> str:
    """Flag or redact unsafe spans using Perspective API.
    Returns the text with spans replaced by '[REDACTED]'.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    # Simple approach: treat the whole text as one span
    req = create_request(text)
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json=req.payload,
        headers={"X-Goog-Api-Key": API_KEY},
    )
    resp.raise_for_status()
    norm = parse_response(resp.json())
    score = norm.scores.get("TOXICITY", 0.0)
    if score >= min_unsafe_score:
        return "[REDACTED]"
    return text
