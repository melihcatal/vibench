import boto3


def embed_log_message(log_message):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=log_message, LanguageCode="en")
    return response["Sentiment"]
