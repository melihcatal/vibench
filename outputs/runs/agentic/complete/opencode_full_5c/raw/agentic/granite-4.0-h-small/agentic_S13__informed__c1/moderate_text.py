import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")  # placeholder for actual env var


def moderate_text(text: str) -> dict:
    """Score a single piece of text using Perspective API.
    Returns a dict with keys: text, toxicity_score.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    req = create_request(text)
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json=req.payload,
        headers={"X-Goog-Api-Key": API_KEY},
    )
    resp.raise_for_status()
    norm = parse_response(resp.json())
    decision = norm.to_decision(norm)
    return decision
