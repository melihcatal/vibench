import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=notes, LanguageCode="en")
    return response["Sentiment"]
