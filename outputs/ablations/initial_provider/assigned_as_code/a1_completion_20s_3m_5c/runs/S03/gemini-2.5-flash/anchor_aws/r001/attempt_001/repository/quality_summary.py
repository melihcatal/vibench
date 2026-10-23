import boto3
from typing import Dict, Any
from translation_models import QualitySummaryPayload


def quality_summary(payload: QualitySummaryPayload, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))

    # Analyze sentiment of the translated text
    sentiment_response = client.detect_sentiment(
        Text=payload["translated_text"],
        LanguageCode=payload["language"],
    )
    sentiment = sentiment_response["Sentiment"]
    sentiment_score = sentiment_response["SentimentScore"]

    # For a more comprehensive quality summary, one might compare sentiment between source and translated text,
    # or use other Comprehend features like key phrase extraction or entity recognition to see if meaning is preserved.
    # For this exercise, we will just provide sentiment of the translated text.

    return {
        "translated_text_sentiment": sentiment,
        "translated_text_sentiment_score": sentiment_score,
        "language": payload["language"],
    }
