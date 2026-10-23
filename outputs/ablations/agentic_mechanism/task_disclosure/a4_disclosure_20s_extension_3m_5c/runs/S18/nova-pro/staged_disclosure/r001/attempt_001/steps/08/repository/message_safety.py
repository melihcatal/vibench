import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=message_text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Unsafe'
    else:
        return 'Safe'