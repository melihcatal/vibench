import boto3

def check_message_safety(message):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=message,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    else:
        return True