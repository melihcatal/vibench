import os
from typing import Dict, Optional
from googleapiclient import discovery

def check_script_for_safety(
    text: str,
    attributes: Optional[list] = None
) -> Optional[Dict]:
    """
    Checks a narration script for unsafe content using the Perspective API.

    Args:
        text: The script content to analyze.
        attributes: A list of attributes to check (e.g., 'TOXICITY', 'SEVERE_TOXICITY').
                    Defaults to ['TOXICITY', 'INSULT', 'THREAT'].

    Returns:
        A dictionary with attribute scores, or None if an error occurs.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    if attributes is None:
        attributes = ['TOXICITY', 'INSULT', 'THREAT']

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {attr: {} for attr in attributes},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in attributes
        }
        return scores
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return None
