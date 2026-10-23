import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text_content: str) -> dict:
    """
    Analyzes text for toxicity using the Google Perspective API.

    This function requires the PERSPECTIVE_API_KEY environment variable.

    Provider: Google Perspective API
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    # The discovery.build call creates a client for the specified API.
    # Provider-identifying signal: "commentanalyzer" service name.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text_content},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        return {'toxicity_score': toxicity_score}
    except HttpError as e:
        print(f"An error occurred with Perspective API: {e}")
        return {'error': str(e)}
