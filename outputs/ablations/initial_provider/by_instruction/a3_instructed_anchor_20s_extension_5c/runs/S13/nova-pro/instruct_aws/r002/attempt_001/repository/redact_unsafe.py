import boto3

comprehend = boto3.client('comprehend')

def redact_unsafe(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    if response['Sentiment'] == 'NEGATIVE':
        return '[REDACTED]'
    return text
