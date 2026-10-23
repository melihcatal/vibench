import boto3

comprehend = boto3.client('comprehend')

def embed_audit_notes(text):
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response['Sentiment']