import os
from googleapiclient import discovery

API_KEY = os.environ.get("PERSPECTIVE_API_KEY")


def check_safety(text: str) -> dict:
    """Checks text for unsafe content using the Perspective API."""
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, value in response["attributeScores"].items():
        scores[attribute] = value["summaryScore"]["value"]

    return scores
