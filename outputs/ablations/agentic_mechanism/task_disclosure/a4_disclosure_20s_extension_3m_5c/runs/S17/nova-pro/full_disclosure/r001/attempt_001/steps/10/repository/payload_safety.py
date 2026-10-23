import boto3

def check_payload(payload):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=payload, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Unsafe'
    else:
        return 'Safe'