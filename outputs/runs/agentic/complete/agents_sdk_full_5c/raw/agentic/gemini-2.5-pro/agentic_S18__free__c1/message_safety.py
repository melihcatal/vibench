import os
from googleapiclient import discovery
from typing import Dict, Optional

def check_text_safety(text: str) -> Optional[Dict]:
    """
    Checks message payload text for unsafe content using Google's Perspective API.

    Args:
        text: The text content to analyze.

    Returns:
        A dictionary with toxicity scores or None on error.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying signal: using the Perspective API client
    try:
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False, # Use dynamic discovery
        )
    except Exception as e:
        print(f"Error building Perspective API client: {e}")
        # Fallback to a predefined discovery URL if dynamic fails
        # This is a common workaround for this library
        discovery_url = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1'
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl=discovery_url
        )


    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        
        scores = {}
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        
        return scores
    except Exception as e:
        print(f"Perspective API request failed: {e}")
        return None
