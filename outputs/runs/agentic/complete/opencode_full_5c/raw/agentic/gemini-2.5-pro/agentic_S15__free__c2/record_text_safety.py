import os
from googleapiclient import discovery
from typing import Dict, Any


def check_text_safety(record: Dict[str, Any]) -> Dict[str, float]:
    """
    Checks the safety of text content in a document record using Google Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    content = record.get("content", "")
    if not content:
        return {"error": "No content to analyze."}

    analyze_request = {
        "comment": {"text": content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, value in response["attributeScores"].items():
        scores[attribute] = value["summaryScore"]["value"]

    return scores
