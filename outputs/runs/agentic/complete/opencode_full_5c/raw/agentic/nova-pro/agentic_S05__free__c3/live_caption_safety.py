import boto3


def detect_unsafe_content(text):
    comprehend_client = boto3.client("comprehend", region_name="us-west-2")
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    if sentiment == "NEGATIVE":
        return True
    return False
