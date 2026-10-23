import boto3

comprehend_client = boto3.client('comprehend')

def check_safety(text):
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment == 'POSITIVE' or sentiment == 'NEUTRAL'