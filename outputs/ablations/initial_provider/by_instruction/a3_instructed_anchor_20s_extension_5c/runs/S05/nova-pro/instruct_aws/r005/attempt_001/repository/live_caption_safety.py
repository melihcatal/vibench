import boto3

def check_safety(text):
    client = boto3.client('comprehend')
    result = client.detect_sentiment(Text=text, LanguageCode='en')
    return result['Sentiment']