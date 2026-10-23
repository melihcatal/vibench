import os
import json
from googleapiclient import discovery
from observability_models import AnnotationSafetyResult


def check_annotation(text: str) -> AnnotationSafetyResult:
    api_key = os.environ.get("GOOGLE_API_KEY")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {
        attr: response["attributeScores"][attr]["summaryScore"]["value"]
        for attr in response["attributeScores"]
    }

    is_safe = all(score < 0.7 for score in scores.values())

    return AnnotationSafetyResult(text=text, is_safe=is_safe, scores=scores)
