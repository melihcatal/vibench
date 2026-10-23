import os
from googleapiclient import discovery

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud's Perspective API.

    Args:
        text: The profile text to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        cache_discovery=False
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

