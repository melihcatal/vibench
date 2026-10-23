import os
from googleapiclient import discovery
from typing import Dict, List

def check_text_safety(text: str) -> Dict[str, float]:
    """
    Checks text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with attribute scores (e.g., TOXICITY, INSULT).
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response['attributeScores'].items():
        scores[attribute] = data['summaryScore']['value']
        
    return scores
