import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts: List[str]) -> List[dict]:
    """Score a list of texts using Perspective API.
    Returns a list of decision dicts, one per input.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    results = []
    for text in texts:
        req = create_request(text)
        resp = requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            json=req.payload,
            headers={"X-Goog-Api-Key": API_KEY},
        )
        resp.raise_for_status()
        norm = parse_response(resp.json())
        results.append(norm.to_decision(norm))
    return results
