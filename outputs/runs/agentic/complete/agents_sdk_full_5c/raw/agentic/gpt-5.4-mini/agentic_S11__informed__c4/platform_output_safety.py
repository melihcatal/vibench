from __future__ import annotations

from typing import Any

import boto3

from model_models import SafetyResult


def check_platform_output_safety(text: str, threshold: float = 0.5) -> SafetyResult:
    client = boto3.client("comprehend")
    response: Any = client.detect_sentiment(Text=text, LanguageCode="en")
    scores = response.get("SentimentScore", {})
    unsafe = max(scores.get("Negative", 0.0), scores.get("Mixed", 0.0)) >= threshold
    return SafetyResult(unsafe=unsafe, score=max(scores.get("Negative", 0.0), scores.get("Mixed", 0.0)), categories=scores, raw=response)
