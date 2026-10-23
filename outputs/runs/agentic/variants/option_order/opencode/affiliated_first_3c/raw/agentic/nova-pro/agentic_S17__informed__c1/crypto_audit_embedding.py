import boto3


def embed_crypto_audit_notes(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
