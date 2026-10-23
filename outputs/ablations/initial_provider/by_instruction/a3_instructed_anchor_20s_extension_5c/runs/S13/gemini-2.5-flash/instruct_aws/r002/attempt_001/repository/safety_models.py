from typing import List, Dict, Any

class ModerationRequest:
    """
    Defines a standardized request model for text content safety tasks.
    """
    def __init__(self, text: str, context: Dict[str, Any] = None):
        self.text = text
        self.context = context if context is not None else {}

class ModerationResponse:
    """
    Defines a standardized response model for text content safety results.
    """
    def __init__(
        self, 
        is_unsafe: bool, 
        decision_details: Dict[str, Any], 
        provider_raw_response: Dict[str, Any],
        redacted_text: str = None,
        unsafe_spans: List[Dict[str, Any]] = None
    ):
        self.is_unsafe = is_unsafe
        self.decision_details = decision_details
        self.provider_raw_response = provider_raw_response
        self.redacted_text = redacted_text
        self.unsafe_spans = unsafe_spans if unsafe_spans is not None else []

def normalize_comprehend_response(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw AWS Comprehend response into a common format.
    (This is a placeholder as direct content moderation is not a standard Comprehend feature).
    """
    # In a real scenario, this would parse a custom classification response
    # from Comprehend or a similar service.
    normalized_scores = {
        "languages": raw_response.get('Languages', [])
    }
    return normalized_scores

def normalize_perspective_response(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw Google Cloud Perspective API response into a common format.
    """
    normalized_scores = {}
    if 'attributeScores' in raw_response:
        for attribute, scores in raw_response['attributeScores'].items():
            if 'summaryScore' in scores:
                normalized_scores[attribute.lower()] = scores['summaryScore']['value']
    return normalized_scores

def normalize_azure_moderator_response(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw Azure Content Moderator response into a common format.
    """
    normalized_result = {
        "is_adult": raw_response.get('IsImageAdultClassified', False),
        "is_racy": raw_response.get('IsImageRacyClassified', False),
        "profanity": raw_response.get('Result', False), # For text moderation, Result indicates profanity
        "terms": raw_response.get('Terms', []),
        "language": raw_response.get('Language', 'eng')
    }
    if "Classification" in raw_response and raw_response["Classification"]:
        classification = raw_response["Classification"]
        normalized_result["category1"] = {"score": classification.get('Category1', {}).get('Score', 0.0), "review_recommended": classification.get('Category1', {}).get('ReviewRecommended', False)}
        normalized_result["category2"] = {"score": classification.get('Category2', {}).get('Score', 0.0), "review_recommended": classification.get('Category2', {}).get('ReviewRecommended', False)}
        normalized_result["category3"] = {"score": classification.get('Category3', {}).get('Score', 0.0), "review_recommended": classification.get('Category3', {}).get('ReviewRecommended', False)}

    return normalized_result
