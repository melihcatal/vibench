import boto3

from speech_client import get_comprehend_client


def moderate_transcript(transcript, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    response = client.detect_sentiment(
        Text=transcript,
        LanguageCode="en"
    )
    sentiment = response["Sentiment"]
    if sentiment == "NEGATIVE":
        return "Moderation failed: Negative sentiment detected."
    return "Moderation passed."