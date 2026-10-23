import os
from googleapiclient import discovery


def check_text_safety(text: str) -> dict:
    """
    Analyzes text for toxic content using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

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

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attribute, value in response["attributeScores"].items():
            scores[attribute] = value["summaryScore"]["value"]
        return scores
    except Exception as e:
        return {"error": str(e)}
