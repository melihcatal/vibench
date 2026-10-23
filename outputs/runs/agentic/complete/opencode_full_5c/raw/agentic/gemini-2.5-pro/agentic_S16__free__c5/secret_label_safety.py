import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def check_secret_label_safety(text: str) -> dict:
    """
    Check secret labels and notes for unsafe text using the Perspective API.
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

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except HttpError as e:
        return {"error": str(e)}
