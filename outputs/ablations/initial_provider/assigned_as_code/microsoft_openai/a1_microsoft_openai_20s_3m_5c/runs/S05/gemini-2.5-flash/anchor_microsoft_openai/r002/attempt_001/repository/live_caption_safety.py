import os
from googleapiclient import discovery

def check_safety(text: str, api_key: str = None) -> dict:
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key must be provided or set in PERSPECTIVE_API_KEY environment variable.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
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
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
