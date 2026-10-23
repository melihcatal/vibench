import boto3


def message_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
