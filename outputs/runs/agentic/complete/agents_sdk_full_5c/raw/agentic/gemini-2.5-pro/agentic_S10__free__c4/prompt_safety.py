import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> dict | None:
    """
    Checks text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with toxicity scores or None on error.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    try:
        # API client setup
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
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        
        return scores

    except HttpError as e:
        print(f"An error occurred with the Perspective API: {e}")
        return None
