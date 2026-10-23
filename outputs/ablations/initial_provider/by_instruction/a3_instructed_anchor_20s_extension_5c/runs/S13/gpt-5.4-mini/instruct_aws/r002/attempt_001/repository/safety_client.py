import os
from typing import Any, Dict

import boto3

from safety_models import SafetyDecision


def get_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_comprehend_client():
    return boto3.client("comprehend", region_name=get_region())


def get_textract_client():
    return boto3.client("textract", region_name=get_region())


def summarize_comprehend_moderation(text: str) -> SafetyDecision:
    client = get_comprehend_client()
    response: Dict[str, Any] = client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response.get("Sentiment", "NEUTRAL")
    scores = response.get("SentimentScore", {})
    unsafe = sentiment in {"NEGATIVE", "MIXED"} and float(scores.get("Negative", 0.0)) >= 0.5
    return SafetyDecision(allow=not unsafe, categories={k.lower(): float(v) for k, v in scores.items()}, raw=response)
