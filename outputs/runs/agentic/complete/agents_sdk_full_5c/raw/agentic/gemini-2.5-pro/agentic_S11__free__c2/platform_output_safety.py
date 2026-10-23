import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> dict:
    """
    Checks platform model output for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing analysis results or an error message.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying client class from googleapiclient
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores
    except HttpError as e:
        return {"error": str(e)}
