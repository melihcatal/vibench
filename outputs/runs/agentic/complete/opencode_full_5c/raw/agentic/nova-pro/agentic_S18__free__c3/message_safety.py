import boto3


def check_unsafe_content(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    return sentiment != "NEGATIVE"
