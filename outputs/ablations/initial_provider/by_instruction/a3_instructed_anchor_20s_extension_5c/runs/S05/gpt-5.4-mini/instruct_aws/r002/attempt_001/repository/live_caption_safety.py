import boto3

from speech_models import TranscriptChunk


def live_caption_safety(chunks):
    client = boto3.client("comprehend", region_name="us-east-1")
    for chunk in chunks:
        client.detect_sentiment(Text=chunk.text, LanguageCode="en")
        yield TranscriptChunk(text=chunk.text, is_final=chunk.is_final)
