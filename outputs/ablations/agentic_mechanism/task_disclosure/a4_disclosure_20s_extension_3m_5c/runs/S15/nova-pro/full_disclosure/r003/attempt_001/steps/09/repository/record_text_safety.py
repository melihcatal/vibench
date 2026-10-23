import boto3

comprehend = boto3.client('comprehend')

def check_unsafe_content(text):
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False