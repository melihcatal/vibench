import boto3


def archive_summary(transcript):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=transcript, LanguageCode="en")
    return response["Sentiment"]
