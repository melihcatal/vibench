import os
from google.cloud import language_v1

# Google Cloud Natural Language client
_language_client = None

def _get_language_client():
    global _language_client
    if _language_client is None:
        _language_client = language_v1.LanguageServiceClient()
    return _language_client

def check_payload_safety(text_payload: str):
    client = _get_language_client()

    document = language_v1.Document(content=text_payload, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a general idea of the content's tone
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    # You can also use other Natural Language API features for more comprehensive safety checks,
    # such as entity analysis, content classification, or custom entity recognition for PII.
    # For this example, we'll focus on sentiment as a basic indicator.

    is_safe = True
    safety_score = sentiment.score # Score ranges from -1.0 (negative) to 1.0 (positive)
    safety_magnitude = sentiment.magnitude # Magnitude indicates the overall strength of emotion
    flagged_reasons = []

    # Example: Flag if the sentiment is very negative and strong
    if safety_score < -0.5 and safety_magnitude > 1.0:
        is_safe = False
        flagged_reasons.append("Strongly negative sentiment detected.")

    # In a real-world scenario, you would integrate with a more robust content moderation API
    # that specifically flags profanity, hate speech, violence, etc.
    # Google Cloud provides services like "Cloud Content Moderation AI" for this, though it's not a public API easily callable here.

    return {
        "is_safe": is_safe,
        "safety_score": safety_score,
        "safety_magnitude": safety_magnitude,
        "flagged_reasons": flagged_reasons,
        "analysis_provider": "Google Cloud Natural Language API"
    }
