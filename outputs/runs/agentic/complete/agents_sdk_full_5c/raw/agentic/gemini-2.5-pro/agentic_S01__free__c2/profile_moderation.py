import os
from googleapiclient import discovery

def moderate_profile_text(text: str) -> dict:
    """
    Analyzes profile text for toxic content using the Google Perspective API.

    Args:
        text: The user-provided text to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The discovery.build method creates a client for the specified API.
    # The Perspective API is identified as 'commentanalyzer'.
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

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response['attributeScores'].items():
        scores[attribute] = data['summaryScore']['value']

    return scores
