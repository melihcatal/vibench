import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_caption_safety(text: str):
    """
    Checks live transcript text for unsafe content using Google's Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary of toxicity scores or an error message.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The discovery.build() function is specific to the Google API Client Library.
    # It dynamically builds a service object for the specified API and version.
    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=api_key,
      static_discovery=False,
    )

    analyze_request = {
      'comment': {'text': text},
      'requestedAttributes': {'TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        return {"toxicity_score": toxicity_score}
    except HttpError as e:
        print(f"An error occurred with Perspective API: {e}")
        return {"error": str(e)}
