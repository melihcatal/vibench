import os
import boto3  # Using AWS Comprehend for toxicity detection (Bedrock Guardrails alternative)
from typing import List, Dict

# Security / moderation settings
MODERATION_THRESHOLD = 0.7  # Adjust confidence threshold as needed

# Initialise Comprehend client (AWS region can be set via env var)
comprehend = boto3.client("comprehend")


def check_message_safety(payload: Dict[str, str]) -> bool:
    """Return True if the message text passes safety checks, else False."""
    text = payload.get("text", "")
    if not text:
        return True  # No text to moderate
    detection = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    # Comprehend returns 'Sentiment' (POSITIVE/NEGATIVE/NEUTRAL/MIXED) and a score per sentiment.
    # For toxic / unsafe content we can also call detect_dominant_language + detect_entities if needed.
    # Here we use a simple heuristic: flag if NEGATIVE sentiment with high confidence.
    sentiment = detection.get("Sentiment")
    sentiment_score = detection.get("SentimentScore", {}).get(sentiment, 0.0)
    if sentiment == "NEGATIVE" and sentiment_score > MODERATION_THRESHOLD:
        print(f"Safety alert: NEGATIVE sentiment ({sentiment_score:.2f}) detected.")
        return False
    return True


# Bulk safety check helper


def batch_check(payloads: List[Dict[str, str]]) -> List[bool]:
    return [check_message_safety(p) for p in payloads]


# Example usage (can be called by downstream services)
if __name__ == "__main__":
    test_cases = [
        {"text": "Great job!"},
        {"text": "You are an idiot and should quit."},
        {"text": "This is neutral content."},
    ]
    results = batch_check(test_cases)
    for t, r in zip(test_cases, results):
        print(f"Text: {t['text']} => Safe: {r}")
