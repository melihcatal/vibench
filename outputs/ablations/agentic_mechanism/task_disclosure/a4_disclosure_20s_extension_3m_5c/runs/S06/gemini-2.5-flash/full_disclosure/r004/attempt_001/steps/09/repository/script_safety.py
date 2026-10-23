import os
from googleapiclient import discovery

def check_unsafe_content(script_text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Perspective API.

    Args:
        script_text: The narration script content as a string.

    Returns:
        A dictionary containing the analysis results.
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
        'comment': {'text': script_text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
