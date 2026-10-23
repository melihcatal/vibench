import boto3
import comprehend

def embed_secret_audit_notes(notes):
    comprehend_client = comprehend.Client()
    response = comprehend_client.detect_sentiment(
        Text=notes,
        LanguageCode='en'
    )
    return response['Sentiment']