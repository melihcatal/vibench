import os
import json
from googleapiclient import discovery
from typing import Dict, Optional

def check_text_safety(text: str) -> Optional[Dict[str, float]]:
    """
    Checks message payload text for unsafe content using the Perspective API.

    Args:
        text: The input text to analyze.

    Returns:
        A dictionary of toxicity scores or None if the API call fails.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Note: googleapiclient is not thread-safe.
    # A new client should be created for each request in a threaded environment.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
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
            'THREAT': {}
        }
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return None
