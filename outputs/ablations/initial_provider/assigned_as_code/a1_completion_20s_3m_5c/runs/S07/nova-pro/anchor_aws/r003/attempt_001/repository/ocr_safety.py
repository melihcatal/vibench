import boto3
from document_client import get_comprehend_client

def ocr_safety(text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']