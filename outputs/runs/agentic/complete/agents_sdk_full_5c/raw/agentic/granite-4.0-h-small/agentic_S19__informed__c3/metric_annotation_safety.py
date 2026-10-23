# [LATER-STEP] metric_annotation_safety.py
import os
import requests
from typing import Dict, Any
from observability_models import MetricRequest

def check_metric_annotations_for_unsafe_text(metric_request: MetricRequest, api_key: str = os.getenv("PERSPECTIVE_API_KEY")):
    """Check free-text metric dimensions/labels for unsafe content using Perspective API.
    Args:
        metric_request: Contains dimensions that may hold free text.
        api_key: Perspective API key; defaults to env var PERSPECTIVE_API_KEY.
    Returns:
        True if any detected toxicity score > 0.5, else False.
    """
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
    payload = {
        "comment": {"text": metric_request.dict(exclude_none=True).get('dimensions', {})},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json=payload,
        headers={"api_key": api_key}
    )
    result = resp.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    toxicity = result.get("value")
    return toxicity and toxicity > 0.5

if __name__ == "__main__":
    # Example: wrap a request that potentially includes user‑generated dimension values
    req = MetricRequest("CPUUtilization", dimensions={"Label": "User Submitted Text"})
    print(check_metric_annotations_for_unsafe_text(req))
