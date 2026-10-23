import os
from googleapiclient import discovery


def moderate_claim(text: str) -> dict:
    """
    Moderates a text string using Google Cloud Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"toxicity_score": toxicity_score}
