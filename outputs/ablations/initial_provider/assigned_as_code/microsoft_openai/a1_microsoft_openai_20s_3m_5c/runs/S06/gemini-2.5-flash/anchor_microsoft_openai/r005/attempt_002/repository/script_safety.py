import boto3
import json


def script_safety(payload, config=None):
    config = config or {}
    
    comprehend = boto3.client(
        service_name='comprehend',
        region_name=config.get('aws_region', 'us-east-1'),
        aws_access_key_id=config.get('aws_access_key_id'),
        aws_secret_access_key=config.get('aws_secret_access_key')
    )
    
    text = payload['text']
    language_code = payload.get('language_code', 'en')
    
    # Detects unsafe content categories using AWS Comprehend
    # For content moderation, usually, a custom classification model or a specific moderation API is used.
    # As a general safety check, we can look for PII or general sentiment.
    # For this exercise, we will use detect_dominant_language and then detect_sentiment as a proxy.
    # A more direct approach would involve custom classification or a dedicated content moderation service.
    
    # AWS Comprehend does have a "DetectModerationLabels" API for images, but not directly for text.
    # For text, you'd typically train a custom classifier or use other services.
    # For the purpose of this exercise, we will check for PII and general sentiment,
    # as these can be indicators of potentially sensitive content.
    
    # Detect PII
    pii_response = comprehend.detect_pii_entities(Text=text, LanguageCode=language_code)
    
    # Detect sentiment as a very basic proxy for safety (e.g., highly negative sentiment might flag content)
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    
    is_safe = True
    safety_flags = []
    
    if pii_response['Entities']:
        is_safe = False
        safety_flags.append({'type': 'PII', 'details': pii_response['Entities']})
    
    if sentiment_response['Sentiment'] == 'NEGATIVE' and sentiment_response['SentimentScore']['Negative'] > 0.8:
        is_safe = False
        safety_flags.append({'type': 'HighNegativeSentiment', 'details': sentiment_response})
        
    return {'is_safe': is_safe, 'safety_flags': safety_flags}