import os
from googleapiclient import discovery
from speech_models import ContentSafetyResult

def check_caption_safety(text: str) -> ContentSafetyResult:
    """
    Checks live transcript text for unsafe content using Google's Perspective API.

    Requires PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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

    attributes = response['attributeScores']
    toxicity_score = attributes['TOXICITY']['summaryScore']['value']
    
    # Define "unsafe" as a toxicity score greater than 0.7
    is_safe = toxicity_score < 0.7
    
    scores = {
        attr: result['summaryScore']['value'] 
        for attr, result in attributes.items()
    }

    return ContentSafetyResult(
        text=text,
        is_safe=is_safe,
        scores=scores
    )
