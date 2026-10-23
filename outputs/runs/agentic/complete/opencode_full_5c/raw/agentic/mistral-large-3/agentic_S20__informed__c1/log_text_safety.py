import os
from googleapiclient import discovery
from google.oauth2 import service_account


def check_log_text_safety(text: str) -> dict:
    """
    Checks log message text for unsafe content using Google Cloud's Perspective API.

    Args:
        text: The log message text to check.

    Returns:
        A dictionary containing toxicity scores and attributes.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
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
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response.get("attributeScores", {})
