import boto3
from storage_client import get_comprehend_client


def asset_metadata_embedding(metadata, text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    return {"metadata": metadata, "sentiment": sentiment}
