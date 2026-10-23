from googleapiclient import discovery
from identity_client import get_google_perspective_api_key


def moderate_text_claim(text: str) -> dict:
    """
    Moderates a free-text claim using the Google Perspective API.
    """
    api_key = get_google_perspective_api_key()

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

    return {
        "text": text,
        "toxicity_score": toxicity_score,
        "flagged": toxicity_score > 0.7,
    }
