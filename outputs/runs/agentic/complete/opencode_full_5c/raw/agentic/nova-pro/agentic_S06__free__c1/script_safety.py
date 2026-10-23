import boto3


def check_safety(script):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_sentiment(Text=script, LanguageCode="en")
    return response["Sentiment"] != "NEGATIVE"
