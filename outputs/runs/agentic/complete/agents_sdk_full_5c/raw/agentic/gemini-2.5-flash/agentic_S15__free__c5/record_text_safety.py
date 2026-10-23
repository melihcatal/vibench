import boto3
import os
from database_client import get_comprehend_client
from database_models import SafetyCheckResult

def check_document_text_safety(document_id: str, text_content: str, language_code: str = 'en') -> SafetyCheckResult:
    """
    Checks user-generated document fields for unsafe content using AWS Comprehend.
    Specifically, this will use `detect_dominant_language` and `detect_pii_entities`
    as well as potentially `detect_sentiment` or `detect_syntax` to infer safety.
    AWS Comprehend does not have a direct 'content moderation' API like Rekognition for images.
    For text content moderation, one would typically use a custom model or a specialized service.
    This implementation will focus on PII detection and a basic sentiment check as proxies for 'safety'.
    """
    comprehend = get_comprehend_client()
    unsafe_detected = False
    moderation_labels = []

    try:
        # Detect PII entities
        pii_response = comprehend.detect_pii_entities(
            Text=text_content,
            LanguageCode=language_code
        )
        if pii_response.get('Entities'):
            unsafe_detected = True
            moderation_labels.append({
                'Type': 'PII_DETECTION',
                'Details': pii_response['Entities']
            })

        # Detect sentiment (e.g., highly negative sentiment could be flagged)
        sentiment_response = comprehend.detect_sentiment(
            Text=text_content,
            LanguageCode=language_code
        )
        sentiment = sentiment_response.get('Sentiment')
        if sentiment in ['NEGATIVE', 'MIXED'] and sentiment_response.get('SentimentScore', {}).get('Negative', 0) > 0.8:
            unsafe_detected = True
            moderation_labels.append({
                'Type': 'HIGHLY_NEGATIVE_SENTIMENT',
                'Details': sentiment_response
            })

        return SafetyCheckResult(
            document_id=document_id,
            unsafe_content_detected=unsafe_detected,
            moderation_labels=moderation_labels
        )
    except Exception as e:
        print(f"Error checking text safety with AWS Comprehend: {e}")
        raise
