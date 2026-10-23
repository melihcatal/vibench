import os
from googleapiclient import discovery

def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing analysis results, including the toxicity score.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Provider-specific client class: discovery.build for 'commentanalyzer'
    # Provider-specific API hostname is implied by the service name
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

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    
    return {"toxicity_score": toxicity_score}
