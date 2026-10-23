from typing import Dict, Any

def apply_safety_thresholds(moderation_result: Dict[str, Any], negative_threshold: float = 0.8) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text based on moderation results.
    For AWS Comprehend sentiment, if the NEGATIVE score exceeds the threshold, it's considered disallowed.
    """
    sentiment_score = moderation_result.get('sentiment_score', {})
    negative_score = sentiment_score.get('Negative', 0.0)

    is_allowed = negative_score < negative_threshold
    
    moderation_result['disallowed_by_threshold'] = not is_allowed
    moderation_result['negative_threshold_applied'] = negative_threshold
    
    return moderation_result
