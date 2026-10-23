import boto3
import json

def check_safety(text: str) -> dict:
    """
    Checks the given text for unsafe content using AWS Comprehend.
    """
    comprehend = boto3.client(
        service_name="comprehend",
        region_name="us-east-1"
    )

    # Example: Detect sentiment, which can indirectly indicate unsafe content if very negative.
    # For more advanced safety, AWS provides Content Moderation with Rekognition for images/videos
    # and custom solutions. For text, sentiment and key phrase extraction are starting points.
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode="en"
    )

    # More comprehensive safety checks would involve custom classification or other AWS AI services.
    # For this example, we'll just return the sentiment.
    return {
        "sentiment": response.get("Sentiment"),
        "sentiment_scores": response.get("SentimentScore")
    }

