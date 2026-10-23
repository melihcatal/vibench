import boto3


def message_summary(message):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_sentiment(Text=message, LanguageCode="en")
    return response
