import boto3


def embed_script(script):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=script, LanguageCode="en")
    return response["Sentiment"]
