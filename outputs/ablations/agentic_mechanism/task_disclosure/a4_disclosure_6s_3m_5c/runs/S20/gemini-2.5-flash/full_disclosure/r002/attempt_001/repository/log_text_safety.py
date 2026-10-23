import os
from googleapiclient import discovery

def check_unsafe_content(log_message: str) -> dict:
    """
    Checks selected log message text for unsafe content using Google Cloud Perspective API.
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
        'comment': {'text': log_message},
        'requestedAttributes': {'TOXICITY': {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

