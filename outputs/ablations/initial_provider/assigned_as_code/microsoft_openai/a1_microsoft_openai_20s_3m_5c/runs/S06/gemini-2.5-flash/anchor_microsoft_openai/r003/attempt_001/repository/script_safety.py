from googleapiclient import discovery
import json
import os

def analyze_safety(text: str, api_key: str) -> dict:
    # Set up the Perspective API client
    # The API key must be enabled for the Perspective API
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en'], # Specify language if known
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
