import os
from googleapiclient import discovery

def check_text_safety(text: str) -> dict:
    """
    Checks corpus text for unwanted content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with analysis results for requested attributes.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response['attributeScores'].items():
        scores[attribute] = data['summaryScore']['value']
        
    return scores
