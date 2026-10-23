import boto3

def check_safety(text):
    comprehend_client = boto3.client('comprehend')
    result = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return result['Sentiment']