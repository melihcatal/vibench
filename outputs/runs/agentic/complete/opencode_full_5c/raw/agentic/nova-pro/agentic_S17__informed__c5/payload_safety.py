import boto3


def payload_safety(plaintext):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_sentiment(Text=plaintext, LanguageCode="en")
    return response["Sentiment"]
