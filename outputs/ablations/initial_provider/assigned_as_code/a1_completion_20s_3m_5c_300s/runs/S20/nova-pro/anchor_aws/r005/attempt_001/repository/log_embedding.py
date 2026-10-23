import boto3

from observability_client import get_observability_client


def embed_log_message(log_message: str, config=None):
    config = config or {}
    comprehend_client = boto3.client("comprehend", region_name=config.get("region"))
    response = comprehend_client.detect_dominant_language(
        Text=log_message,
    )
    language_code = response["Languages"][0]["LanguageCode"]
    embeddings = comprehend_client.detect_sentiment(
        Text=log_message,
        LanguageCode=language_code,
    )
    return embeddings["Sentiment"]
