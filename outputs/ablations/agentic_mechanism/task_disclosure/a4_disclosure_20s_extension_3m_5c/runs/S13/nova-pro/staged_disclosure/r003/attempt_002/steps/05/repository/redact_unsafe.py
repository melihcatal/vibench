import boto3

def redact_unsafe_spans(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    if response['Sentiment'] == 'NEGATIVE':
        return '[REDACTED]'
    else:
        return text