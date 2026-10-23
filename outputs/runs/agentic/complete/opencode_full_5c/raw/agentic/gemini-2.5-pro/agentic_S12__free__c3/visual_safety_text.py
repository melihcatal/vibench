import os
from googleapiclient import discovery
from vision_models import ImageLabel

API_KEY = os.environ["PERSPECTIVE_API_KEY"]


def check_text_safety(labels: list[ImageLabel]) -> dict:
    """Checks generated visual labels for unsafe text using Perspective API."""
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    results = {}
    for label in labels:
        analyze_request = {
            "comment": {"text": label.description},
            "requestedAttributes": {"TOXICITY": {}},
        }

        response = client.comments().analyze(body=analyze_request).execute()

        toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        results[label.description] = toxicity_score > 0.7

    return results
