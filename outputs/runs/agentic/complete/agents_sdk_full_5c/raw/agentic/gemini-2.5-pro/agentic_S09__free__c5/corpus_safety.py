import os
from typing import Dict, Any
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for harmful content using Google's Perspective API.

    Args:
        text: The input text to analyze.

    Returns:
        A dictionary containing attribute scores from the API.
    """
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying client class from googleapiclient
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
    except HttpError as e:
        return {"error": f"Perspective API error: {e}"}

