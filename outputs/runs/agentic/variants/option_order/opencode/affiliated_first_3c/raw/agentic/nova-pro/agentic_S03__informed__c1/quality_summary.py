import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def quality_summary(text):
    result = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return result["Sentiment"]
