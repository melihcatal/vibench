import boto3


def message_safety(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
