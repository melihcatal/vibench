import os
import json
from googleapiclient import discovery


def script_safety(text: str):
    """
    Analyzes text for unsafe content using the Perspective API.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary of attribute scores from the Perspective API.
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

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    return response
