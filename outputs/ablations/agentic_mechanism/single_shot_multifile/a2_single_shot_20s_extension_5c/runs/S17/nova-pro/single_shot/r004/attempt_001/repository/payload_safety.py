import boto3

from security_client import get_comprehend_client

def get_comprehend_client():
    return boto3.client('comprehend')

def payload_safety(text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']!= 'NEGATIVE'