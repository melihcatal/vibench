import boto3

from storage_client import get_s3_client


def embed_metadata(metadata, config=None):
    config = config or {}
    comprehend_client = boto3.client('comprehend', region_name=config.get('region'))

    response = comprehend_client.detect_sentiment(Text=metadata, LanguageCode='en')
    return response