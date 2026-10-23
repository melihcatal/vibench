import boto3

def embed_crypto_audit_notes(text):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']