from googleapiclient import discovery
import json

def check_unsafe_text(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud's Perspective API.

    Args:
        text: The free-text to analyze.

    Returns:
        A dictionary containing the analysis results from Perspective API.
    """
    API_KEY = "YOUR_PERSPECTIVE_API_KEY"  # Replace with your actual API key
    
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
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

