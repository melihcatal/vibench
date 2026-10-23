
import os
from googleapiclient import discovery

def check_unsafe_content(text: str) -> dict:
    """
    Checks localized copy for unsafe content using Google Cloud Perspective API.

    Args:
        text: The text content to analyze.

    Returns:
        A dictionary containing the analysis results from Perspective API.
    """

    # It's recommended to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file, or use an API key.
    # For more information: https://cloud.google.com/docs/authentication/production
    # Example using an API key:
    # API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    # if not API_KEY:
    #     raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    # client = discovery.build(
    #     "commentanalyzer",
    #     "v1alpha1",
    #     developerKey=API_KEY,
    #     cache_discovery=False
    # )

    # Using default credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS env var)
    # Ensure 'google-api-python-client' and 'google-auth' are installed.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        cache_discovery=False
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

