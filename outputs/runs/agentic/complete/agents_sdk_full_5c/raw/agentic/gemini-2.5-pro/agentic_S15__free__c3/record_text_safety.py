import os
from typing import Dict, Any
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def record_text_safety(record: Dict[str, Any], text_field: str) -> Dict[str, float]:
    """
    Checks user-generated text fields for unsafe content using Google's Perspective API.

    Args:
        record: The document record.
        text_field: The key of the text field to analyze.

    Returns:
        A dictionary of toxicity scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    text_to_analyze = record.get(text_field)
    if not text_to_analyze:
        return {}

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text_to_analyze},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'INSULT': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        return scores
    except HttpError as e:
        print(f"Perspective API error: {e}")
        return {}
