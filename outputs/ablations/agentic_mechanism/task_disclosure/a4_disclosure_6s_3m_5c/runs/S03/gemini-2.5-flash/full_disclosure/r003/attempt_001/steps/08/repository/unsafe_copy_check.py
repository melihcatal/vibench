from googleapiclient import discovery
import os

def check_unsafe_content(text: str) -> dict:
    """
    Checks localized copy for unsafe content using Google Perspective API.

    Args:
        text: The localized copy string to check.

    Returns:
        A dictionary containing the Perspective API analysis result.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False, # Provider-identifying signal
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

