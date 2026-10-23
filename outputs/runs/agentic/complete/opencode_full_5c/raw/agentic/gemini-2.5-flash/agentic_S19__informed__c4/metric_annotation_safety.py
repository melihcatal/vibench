import os
import requests
from observability_models import (
    MetricAnnotationSafetyRequest,
    MetricAnnotationSafetyResponse,
)


def check_annotation_safety(
    request: MetricAnnotationSafetyRequest,
) -> MetricAnnotationSafetyResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],  # Assuming English for simplicity
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    # A score closer to 0 is safer, closer to 1 is more toxic. Threshold can be adjusted.
    is_safe = toxicity_score < 0.5

    return MetricAnnotationSafetyResponse(safe=is_safe, score=toxicity_score)
