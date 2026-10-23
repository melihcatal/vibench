import boto3
from observability_client import get_comprehend_client

comprehend = get_comprehend_client()

def check_metric_annotation_safety(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']!= 'NEGATIVE'