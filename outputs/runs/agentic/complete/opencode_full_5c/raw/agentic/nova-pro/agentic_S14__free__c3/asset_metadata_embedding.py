import boto3


def asset_metadata_embedding(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response
