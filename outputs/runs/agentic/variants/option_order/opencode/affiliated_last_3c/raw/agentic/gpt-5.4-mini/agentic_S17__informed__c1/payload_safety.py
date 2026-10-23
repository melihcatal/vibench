import boto3

from security_models import PayloadSafetyResult, normalize_text, response_map


def payload_safety(text):
    comprehend = boto3.client('comprehend')
    content = normalize_text(text)
    result = comprehend.detect_sentiment(Text=content, LanguageCode='en')
    safe = result.get('Sentiment') in {'POSITIVE', 'NEUTRAL'}
    reasons = [] if safe else [result.get('Sentiment', 'UNKNOWN')]
    return response_map(text=content, is_safe=safe, reasons=reasons)
