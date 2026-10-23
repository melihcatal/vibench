import boto3


def summarize_moderation_decisions(decisions):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=decisions, LanguageCode="en")
    return response["Sentiment"]
