from __future__ import annotations

import os

import boto3

from observability_models import SafetyCheckResponse


def metric_annotation_safety(text: str) -> SafetyCheckResponse:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    client = boto3.client("comprehend", region_name=region)
    entities = client.detect_pii_entities(Text=text, LanguageCode="en").get("Entities", [])
    is_safe = len(entities) == 0
    reason = None if is_safe else "Detected potentially sensitive or unsafe text"
    return SafetyCheckResponse(text=text, is_safe=is_safe, reason=reason)
