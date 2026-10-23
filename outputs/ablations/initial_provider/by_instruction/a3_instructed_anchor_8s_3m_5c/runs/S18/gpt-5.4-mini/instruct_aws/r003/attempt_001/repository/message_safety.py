import boto3


def message_safety(text):
    client = boto3.client("comprehend", region_name="us-east-1")
    return client.detect_sentiment(Text=text, LanguageCode="en")
