import boto3
import os


def check_payload_safety(payload, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")

    comprehend_client = boto3.client("comprehend", region_name=region_name)

    text = payload["text"]

    # Detect unsafe content (toxicity, insults, etc.)
    # Note: AWS Comprehend has specific APIs for different types of content moderation
    # For a general safety check, we might look for sentiment, PII, or custom entity recognition.
    # Here, we will use detect_sentiment as a proxy for a basic safety check,
    # and also detect_pii_entities as an example of sensitive data detection.

    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode="en")

    is_unsafe = False
    safety_notes = []

    if sentiment_response["Sentiment"] == "NEGATIVE":
        is_unsafe = True
        safety_notes.append("Negative sentiment detected.")

    if pii_response["Entities"]:
        is_unsafe = True
        safety_notes.append("Personally Identifiable Information (PII) detected.")

    return {"is_unsafe": is_unsafe, "safety_notes": safety_notes, "sentiment": sentiment_response["Sentiment"], "pii_entities": pii_response["Entities"]}
