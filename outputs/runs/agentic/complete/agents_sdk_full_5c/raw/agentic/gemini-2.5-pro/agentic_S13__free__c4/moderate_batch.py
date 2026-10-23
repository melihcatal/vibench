"""Moderates a batch of user messages using Google Perspective API."""
import time
from typing import List, Dict
from safety_client import get_perspective_client
from safety_models import ModerationResult


def moderate_batch_perspective(messages: List[str]) -> Dict[str, ModerationResult]:
    """
    Moderates a batch of messages using the Google Perspective API.

    Note: The Perspective API does not have a native batch endpoint,
    so we send requests sequentially with a delay to respect rate limits.

    Args:
        messages: A list of strings to moderate.

    Returns:
        A dictionary mapping each message to its moderation result.
    """
    client = get_perspective_client()
    results = {}
    
    # These are some of the attributes the Perspective API can analyze
    analyze_request_body = {
        'comment': {'text': ''},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    for msg in messages:
        analyze_request_body['comment']['text'] = msg
        
        response = client.comments().analyze(body=analyze_request_body).execute()
        
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        
        # A simple flagging logic: flag if any score is above 0.7
        flagged = any(score > 0.7 for score in scores.values())
        
        results[msg] = ModerationResult(
            flagged=flagged,
            categories={cat: score > 0.7 for cat, score in scores.items()},
            scores=scores,
            details="Google Perspective API"
        )
        time.sleep(1) # Respect API rate limits for non-batch processing

    return results
