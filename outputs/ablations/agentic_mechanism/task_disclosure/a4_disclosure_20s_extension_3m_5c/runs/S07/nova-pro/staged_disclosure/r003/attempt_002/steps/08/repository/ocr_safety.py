import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False