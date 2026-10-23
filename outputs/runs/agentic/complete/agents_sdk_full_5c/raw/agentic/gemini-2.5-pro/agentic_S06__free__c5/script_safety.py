import os
from googleapiclient import discovery

def check_script_safety(text: str, threshold: float = 0.7) -> dict:
    """
    Checks narration scripts for unsafe content using the Perspective API.

    Args:
        text: The script content to analyze.
        threshold: The score threshold for flagging content.

    Returns:
        A dictionary of toxicity scores and a flag indicating if it's safe.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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

    response = client.comments().analyze(body=analyze_request).execute()
    
    scores = {}
    safe = True
    for attr, value in response['attributeScores'].items():
        score = value['summaryScore']['value']
        scores[attr] = score
        if score > threshold:
            safe = False
            
    return {"safe": safe, "scores": scores}
