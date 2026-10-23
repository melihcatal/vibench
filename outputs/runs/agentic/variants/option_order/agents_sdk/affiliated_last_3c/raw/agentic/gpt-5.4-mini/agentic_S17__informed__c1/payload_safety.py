from __future__ import annotations

import boto3


def payload_safety(text: str, region_name: str | None = None) -> dict:
    comprehend = boto3.client("comprehend", region_name=region_name)
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    unsafe = response.get("Sentiment") in {"NEGATIVE", "MIXED"} and response.get("SentimentScore", {}).get("Negative", 0.0) > 0.7
    return {"provider": "Amazon Comprehend", "unsafe": unsafe, "sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}
