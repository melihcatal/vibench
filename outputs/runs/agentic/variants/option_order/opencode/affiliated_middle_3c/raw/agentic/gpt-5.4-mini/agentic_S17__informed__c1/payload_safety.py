import boto3
from security_client import get_region_name

def payload_safety(decrypted_text: str) -> dict:
    client = boto3.client('comprehend', region_name=get_region_name())
    response = client.detect_sentiment(Text=decrypted_text[:4500], LanguageCode='en')
    unsafe = response.get('Sentiment') in {'NEGATIVE', 'MIXED'} and response.get('SentimentScore', {}).get('Negative', 0) > 0.6
    return {'provider': 'aws_comprehend', 'unsafe': unsafe, 'sentiment': response.get('Sentiment')}
