import boto3

from security_client import aws_region


def payload_safety(text: str) -> dict:
    comprehend = boto3.client("comprehend", region_name=aws_region())
    sentiment = comprehend.detect_sentiment(Text=text[:5000], LanguageCode="en")
    return {"unsafe": sentiment.get("Sentiment") in {"NEGATIVE", "MIXED"}, "sentiment": sentiment.get("Sentiment"), "scores": sentiment.get("SentimentScore", {})}
