import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def summarize_transcript(transcript):
    response = comprehend.detect_sentiment(Text=transcript, LanguageCode="en")
    return response["Sentiment"]
