import boto3


def record_summary(document):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=document, LanguageCode="en")
    return response["Sentiment"]
