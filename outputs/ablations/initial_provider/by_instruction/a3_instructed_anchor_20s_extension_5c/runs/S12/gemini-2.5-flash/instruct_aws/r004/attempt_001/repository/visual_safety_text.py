import os
from typing import Dict, Any, List
from googleapiclient import discovery

def visual_safety_text(text_content: str) -> Dict[str, Any]:
    """
    Checks generated visual labels and descriptions for unsafe text using Google Perspective API.

    Args:
        text_content: The combined text content (labels, descriptions, detected text) to check.

    Returns:
        A dictionary containing the safety scores for various attributes.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
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
        'comment': {'text': text_content},
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

    attribute_scores = {}
    for attribute, scores in response.get('attributeScores', {}).items():
        attribute_scores[attribute] = scores.get('summaryScore', {}).get('value')

    return {"safety_scores": attribute_scores}
