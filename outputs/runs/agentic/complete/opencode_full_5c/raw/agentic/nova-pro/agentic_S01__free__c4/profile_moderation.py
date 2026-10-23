import boto3


def moderate_profile_text(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
