import boto3


def embed_moderation_rationales(rationale):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=rationale, LanguageCode="en")
    return response["Sentiment"]
