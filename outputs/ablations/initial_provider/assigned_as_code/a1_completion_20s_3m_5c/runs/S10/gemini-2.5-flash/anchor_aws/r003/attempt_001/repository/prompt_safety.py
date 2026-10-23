import boto3
import os

def check_safety(payload, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    client = boto3.client("comprehend", region_name=region)

    text_to_analyze = payload.get("text", "")
    language_code = payload.get("language_code", "en") # e.g., 'en', 'es', 'fr'

    # Detect unsafe content using Comprehend's DetectDominantLanguage and DetectSentiment as a proxy
    # For more advanced safety, a custom content moderation model or a more specific Comprehend feature might be needed.
    # As an example, we'll check for general sentiment and PII.

    sentiment_response = client.detect_sentiment(Text=text_to_analyze, LanguageCode=language_code)
    sentiment = sentiment_response["Sentiment"]
    sentiment_score = sentiment_response["SentimentScore"]

    # You could also use detect_pii_entities for privacy concerns, or custom classification models.
    # pii_response = client.detect_pii_entities(Text=text_to_analyze, LanguageCode=language_code)

    is_unsafe = False
    safety_flags = []

    # Example: Flag if sentiment is overwhelmingly negative
    if sentiment == "NEGATIVE" and sentiment_score["Negative"] > 0.9:
        is_unsafe = True
        safety_flags.append("Strongly negative sentiment detected")

    # Add more sophisticated safety checks here as needed, potentially integrating with other AWS services

    return {
        "is_unsafe": is_unsafe,
        "safety_flags": safety_flags,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
    }
