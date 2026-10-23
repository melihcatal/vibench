import os
from typing import Dict, Any

from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Checks platform model output for unsafe content using Google's Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The Perspective API is a Google Cloud service for content analysis
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except HttpError as e:
        print(f"An error occurred with Perspective API: {e}")
        return {}
