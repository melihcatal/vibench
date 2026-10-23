from __future__ import annotations

from typing import Dict

import boto3

from security_models import SafetyCheckResult, coerce_text


AWS_COMPREHEND_PROVIDER = "boto3:comprehend"


def payload_safety(text: str, region: str = "us-east-1") -> SafetyCheckResult:
    client = boto3.client("comprehend", region_name=region)
    response = client.detect_sentiment(Text=coerce_text(text), LanguageCode="en")
    sentiment = response.get("Sentiment", "UNKNOWN")
    score_map: Dict[str, float] = response.get("SentimentScore", {})
    unsafe = sentiment in {"NEGATIVE", "MIXED"} and float(score_map.get("Negative", 0.0)) > 0.5
    return SafetyCheckResult(unsafe=unsafe, score=float(score_map.get("Negative", 0.0)), labels=score_map, raw={"provider": AWS_COMPREHEND_PROVIDER, **response})
