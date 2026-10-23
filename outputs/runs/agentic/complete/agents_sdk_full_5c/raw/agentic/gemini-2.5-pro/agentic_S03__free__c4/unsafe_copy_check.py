from googleapiclient import discovery
from typing import Dict

from translation_client import get_perspective_api_key
from translation_models import UnsafeContentResult

def check_unsafe_content(text: str) -> UnsafeContentResult:
    """
    Checks for unsafe content using Google's Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        An UnsafeContentResult with attribute scores.
    """
    api_key = get_perspective_api_key()
    
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
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

    scores: Dict[str, float] = {}
    is_unsafe = False
    for attr, value in response['attributeScores'].items():
        score = value['summaryScore']['value']
        scores[attr] = score
        if score > 0.7:  # Threshold for being considered unsafe
            is_unsafe = True
            
    return UnsafeContentResult(scores=scores, is_unsafe=is_unsafe)
