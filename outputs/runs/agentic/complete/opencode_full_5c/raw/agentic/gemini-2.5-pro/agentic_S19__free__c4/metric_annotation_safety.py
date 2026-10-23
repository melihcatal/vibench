import os
from googleapiclient import discovery
from observability_models import SafetyCheckRequest


def check_annotation_safety(request: SafetyCheckRequest) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {
        "text": request.text,
        "toxicity_score": toxicity_score,
        "is_safe": toxicity_score < 0.7,
    }
