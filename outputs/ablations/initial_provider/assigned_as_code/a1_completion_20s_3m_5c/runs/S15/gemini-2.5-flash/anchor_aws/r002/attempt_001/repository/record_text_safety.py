import os

import boto3


def check_text_safety(text):
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    comprehend = boto3.client("comprehend", region_name=region_name)

    # Using Comprehend for basic text safety checks like sentiment and language detection.
    # For more advanced content moderation, a dedicated service would be ideal.
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    language_response = comprehend.detect_dominant_language(Text=text)

    sentiment = sentiment_response["Sentiment"]
    sentiment_scores = sentiment_response["SentimentScore"]
    dominant_language = language_response["Languages"][0]["LanguageCode"]

    # A very basic heuristic for "unsafe" could be strongly negative sentiment,
    # but real safety checks are far more complex.
    is_potentially_unsafe = sentiment == "NEGATIVE" and sentiment_scores["Negative"] > 0.8

    return {
        "sentiment": sentiment,
        "sentiment_scores": sentiment_scores,
        "dominant_language": dominant_language,
        "is_potentially_unsafe": is_potentially_unsafe,
        "provider": "AWS Comprehend",
    }
