import boto3


def profile_moderation(text):
    comprehend = boto3.client("comprehend")
    result = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return result["Sentiment"]
