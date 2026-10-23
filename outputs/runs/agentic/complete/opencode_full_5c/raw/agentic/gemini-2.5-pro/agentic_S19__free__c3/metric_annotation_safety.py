import os
import requests
from observability_models import UnsafeTextCheckRequest, UnsafeTextCheckResult


def check_annotation_safety(request: UnsafeTextCheckRequest) -> UnsafeTextCheckResult:
    """
    Checks for unsafe text using the Google Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": request.text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    scores = {
        attr: data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in data["attributeScores"]
    }

    is_unsafe = scores.get("TOXICITY", 0.0) > 0.7

    return UnsafeTextCheckResult(text=request.text, is_unsafe=is_unsafe, scores=scores)
