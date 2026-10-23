import boto3
from translation_client import get_comprehend_client

def quality_summary(payload, config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))
    response = client.detect_sentiment(
        Text=payload["translated_text"],
        LanguageCode=payload["target_language"],
    )
    return {
        "sentiment": response["Sentiment"],
        "sentiment_scores": response["SentimentScore"],
        "translated_text": payload["translated_text"],
        "target_language": payload["target_language"],
    }