import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")

THRESHOLDS = {
    "TOXICITY": 0.5,  # example: allow if score < 0.5
}


def safety_threshold(text: str) -> dict:
    """Apply category thresholds to decide whether to allow text.
    Returns dict with decision and reason.
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
    decision = "ALLOW"
    reasons = {}
    for category, thresh in THRESHOLDS.items():
        score = norm.scores.get(category)
        reasons[category] = score or 0.0
        if score and score >= thresh:
            decision = "REJECT"
            break
    return {"text": text, "decision": decision, "reasons": reasons}
