import boto3

from speech_client import get_speech_client


def transcript_embedding(transcript, config=None):
    client = get_speech_client(config)
    comprehend_client = boto3.client('comprehend', region_name=config.get('region'))
    response = comprehend_client.detect_sentiment(
        Text=transcript,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    embedding = f"Sentiment: {sentiment}"
    return embedding