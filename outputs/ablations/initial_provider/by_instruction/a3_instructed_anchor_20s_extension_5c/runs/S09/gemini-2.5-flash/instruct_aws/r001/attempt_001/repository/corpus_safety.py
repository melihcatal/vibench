import boto3
import os
import json

def check_corpus_safety(text: str) -> dict:
    """
    Checks corpus text for safety before embedding using AWS Comprehend.
    """
    comprehend = boto3.client(
        service_name="comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Using detect_sentiment as a proxy for safety check, as Comprehend doesn't have a direct 'safety' API
    # For a more robust safety check, one might integrate with a dedicated content moderation service.
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en') # Assuming English for simplicity
    return {
        "sentiment": response["Sentiment"],
        "sentiment_scores": response["SentimentScore"],
        "safe_for_embedding": response["Sentiment"] not in ["NEGATIVE", "MIXED"]
    }
