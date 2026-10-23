import boto3

from speech_client import get_comprehend_client


def transcript_embedding(transcript, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    response = client.detect_sentiment(
        Text=transcript,
        LanguageCode="en"
    )
    sentiment = response["Sentiment"]
    return sentiment