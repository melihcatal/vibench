import os
from googleapiclient import discovery
from observability_models import AnnotationSafetyResult


def check_annotation_safety(text: str) -> AnnotationSafetyResult:
    """
    Checks free-text annotations for safety using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {
        attr: response["attributeScores"][attr]["summaryScore"]["value"]
        for attr in response["attributeScores"]
    }

    is_safe = all(score < 0.7 for score in scores.values())

    return AnnotationSafetyResult(text=text, scores=scores, safe=is_safe)
