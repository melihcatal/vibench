import os
from security_client import get_comprehend_client


def check_label_safety(text: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using Amazon Comprehend.
    This example uses sentiment detection as a proxy for 'safety' check,
    as direct content moderation usually involves more specialized services.
    """
    client = get_comprehend_client()
    try:
        # Detect dominant language first to ensure correct sentiment analysis
        language_response = client.detect_dominant_language(Text=text)
        dominant_language = language_response["Languages"][0]["LanguageCode"]

        sentiment_response = client.detect_sentiment(
            Text=text, LanguageCode=dominant_language
        )
        return {
            "sentiment": sentiment_response["Sentiment"],
            "sentiment_scores": sentiment_response["SentimentScore"],
            "dominant_language": dominant_language,
        }
    except Exception as e:
        raise RuntimeError(f"Error checking label safety with Comprehend: {e}")
