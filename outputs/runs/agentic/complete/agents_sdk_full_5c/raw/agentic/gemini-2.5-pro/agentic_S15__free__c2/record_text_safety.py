import os
from typing import Dict, Any
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text_content: str) -> Dict[str, float]:
    """
    Checks user-generated text for unsafe content using Google's Perspective API.

    :param text_content: The text to analyze.
    :return: A dictionary of safety attributes and their scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying signal: 'commentanalyzer' is the Perspective API service name.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
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
    except HttpError as e:
        print(f"Error from Perspective API: {e}")
        return {}

