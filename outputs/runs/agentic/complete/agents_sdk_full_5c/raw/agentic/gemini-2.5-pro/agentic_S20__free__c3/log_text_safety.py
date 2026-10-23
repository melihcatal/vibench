import os
from typing import Dict, Optional

from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_log_content_safety(text: str) -> Optional[Dict[str, float]]:
    """
    Analyzes log message text for unsafe content using the Google Perspective API.

    Args:
        text: The log message to analyze.

    Returns:
        A dictionary of toxicity scores or None if an error occurs.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        print("Error: PERSPECTIVE_API_KEY environment variable not set.")
        return None

    try:
        # The API client is built dynamically based on the discovery document.
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False, # Use dynamic discovery
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

        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores

    except HttpError as e:
        print(f"An HTTP error occurred with Perspective API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
