import os
from googleapiclient import discovery # Google Cloud Perspective API client

def check_unsafe_copy(text: str) -> dict:
    # Initialize the Perspective API client
    # Ensure GOOGLE_API_KEY environment variable is set for API key authentication
    # Or use service account for OAuth 2.0
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Perspective API.")

    # The service name and version for Perspective API are 'commentanalyzer' and 'v1alpha1'
    # The hostname is 'commentanalyzer.googleapis.com'
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
