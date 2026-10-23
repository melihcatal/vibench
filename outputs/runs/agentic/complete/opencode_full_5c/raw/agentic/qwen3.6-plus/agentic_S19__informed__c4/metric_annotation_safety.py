import os
import requests
from typing import Optional

from observability_models import (
    AnnotationSafetyRequest,
    AnnotationSafetyResponse,
)

PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1"


def get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable is required for Perspective API"
        )
    return api_key


def check_annotation_safety(
    request: AnnotationSafetyRequest,
) -> AnnotationSafetyResponse:
    api_key = get_perspective_api_key()
    url = f"{PERSPECTIVE_API_BASE}/comments:analyze"
    params = {"key": api_key}
    payload = {
        "comment": {"text": request.text},
        "requestedAttributes": {attr: {} for attr in request.categories},
        "languages": ["en"],
        "spanAnnotations": False,
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, params=params, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    scores = {}
    flagged_categories = []
    attribute_scores = data.get("attributeScores", {})
    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = round(score, 4)
        if score >= 0.5:
            flagged_categories.append(attr_name)
    is_safe = len(flagged_categories) == 0
    return AnnotationSafetyResponse(
        text=request.text,
        scores=scores,
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        status="ok",
    )


if __name__ == "__main__":
    req = AnnotationSafetyRequest(
        text="This dashboard monitors production server health. All systems nominal.",
        categories=["TOXICITY", "SEVERE_TOXICITY", "THREAT", "INSULT"],
    )
    result = check_annotation_safety(req)
    print(f"Safe: {result.is_safe}")
    print(f"Scores: {result.scores}")
