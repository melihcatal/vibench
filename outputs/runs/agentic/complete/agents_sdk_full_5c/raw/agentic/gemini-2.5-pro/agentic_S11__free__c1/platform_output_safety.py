from googleapiclient import discovery
from model_client import GOOGLE_API_KEY

def check_text_safety_perspective(text: str) -> dict:
    """
    Checks text for harmful content using Google's Perspective API.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY for Perspective API not set.")

    # Provider-specific client class: googleapiclient.discovery.Resource
    # Provider-specific API hostname is implicitly contained in the discovery process
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=GOOGLE_API_KEY,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    return response
