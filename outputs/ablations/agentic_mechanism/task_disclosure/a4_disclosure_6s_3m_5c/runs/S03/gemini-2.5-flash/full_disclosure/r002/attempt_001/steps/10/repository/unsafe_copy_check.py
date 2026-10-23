
from googleapiclient import discovery
import os

def check_unsafe_content(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Cloud's Perspective API.

    Args:
        text: The localized copy string to check.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    # Replace with your API key
    API_KEY = os.getenv("PERSPECTIVE_API_KEY")
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

