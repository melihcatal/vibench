import os
from googleapiclient import discovery


def corpus_safety(text: str) -> dict:
    """
    Checks corpus text for safety before embedding using Google's Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"toxicity_score": toxicity_score}
