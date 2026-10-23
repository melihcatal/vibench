import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def summarize_text(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
