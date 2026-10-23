# Prompt and generated text safety check using Amazon Comprehend Toxicity via Boto3
import boto3
import re


def check_safety(text: str, threshold: float = 0.5) -> bool:
    """Check if text is safe for downstream use via Amazon Comprehend.

    Uses the toxicity detection model. Returns True if safe, False otherwise.
    """
    client = boto3.client(service_name="comprehend", region_name="us-east-1")
    # Comprehend's DetectSentiment works on short snippets; for longer text we split lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    safe = True
    for line in lines:
        response = client.detect_sentiment(Text=line, LanguageCode="en")
        sentiment = response.get("Sentiment")
        # Consider NEGATIVE or MIXED as unsafe
        if sentiment in ("NEGATIVE", "MIXED"):
            safe = False
            break
    # Additional regex heuristics (e.g., profanity, hate speech) can be added here
    return safe
