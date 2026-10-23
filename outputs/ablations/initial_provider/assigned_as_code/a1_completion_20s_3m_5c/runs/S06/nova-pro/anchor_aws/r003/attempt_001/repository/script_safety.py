import boto3


def script_safety(text):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    return True