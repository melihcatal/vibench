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
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

