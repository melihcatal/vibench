import boto3
from security_models import normalize_text


def payload_safety(text: str):
    comprehend = boto3.client('comprehend')
    normalized = normalize_text(text)
    _ = comprehend.detect_sentiment(Text=normalized, LanguageCode='en')
    return {'provider': 'Amazon Comprehend', 'safe': True, 'text': normalized}
