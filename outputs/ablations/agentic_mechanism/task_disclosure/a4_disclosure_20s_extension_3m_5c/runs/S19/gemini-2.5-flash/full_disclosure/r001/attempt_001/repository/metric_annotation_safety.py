import os
from googleapiclient import discovery

def check_unsafe_text(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud's Perspective API.

    Args:
        text: The free-text label or annotation to check.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

