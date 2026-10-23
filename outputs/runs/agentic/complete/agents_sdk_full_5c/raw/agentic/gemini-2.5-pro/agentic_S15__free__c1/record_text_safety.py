import os
import json
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> dict:
    """
    Checks user-generated text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with toxicity scores.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # The Perspective API client is built using the discovery service
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        return scores
    except HttpError as e:
        print(f"An error occurred with the Perspective API: {e}")
        error_content = json.loads(e.content)
        return {"error": error_content.get("error", {}).get("message", "Unknown error")}
