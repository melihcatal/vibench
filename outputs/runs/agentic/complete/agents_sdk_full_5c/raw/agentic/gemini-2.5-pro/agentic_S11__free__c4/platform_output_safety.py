import os
from googleapiclient import discovery

def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using Google's Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing the analysis scores from the Perspective API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Provider-specific client class from the googleapiclient library
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
        'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, value in response['attributeScores'].items():
        scores[attribute] = value['summaryScore']['value']

    return scores
