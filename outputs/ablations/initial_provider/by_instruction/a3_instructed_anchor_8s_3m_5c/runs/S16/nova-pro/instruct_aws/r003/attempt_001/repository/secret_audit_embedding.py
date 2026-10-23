import boto3

def embed_secret_audit_notes(notes):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=notes, LanguageCode='en')
    return response['Sentiment']