import os
from typing import List, Dict, Any
from googleapiclient import discovery
from safety_models import ModerationResponse, BatchModerationResponse

def moderate_batch(messages: List[str]) -> BatchModerationResponse:
    """
    Moderates a batch of user messages using Google's Perspective API.

    Args:
        messages: A list of strings to moderate.

    Returns:
        A BatchModerationResponse containing the result for each message.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not found in environment.")

    # Note: googleapiclient is not thread-safe.
    # For production, create a new client per thread/request.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    results = []
    for msg in messages:
        analyze_request = {
            'comment': {'text': msg},
            'requestedAttributes': {'TOXICITY': {}}
        }
        
        response = client.comments().analyze(body=analyze_request).execute()
        
        summary_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        is_safe = summary_score < 0.7  # Example threshold

        results.append(
            ModerationResponse(
                is_safe=is_safe,
                scores={'toxicity': summary_score},
                raw_response=response
            )
        )
            
    return BatchModerationResponse(results=results)
