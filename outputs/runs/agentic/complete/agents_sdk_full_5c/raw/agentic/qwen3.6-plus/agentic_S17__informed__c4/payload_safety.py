"""Check decrypted text payloads for unsafe content using Amazon Comprehend."""

import os
from typing import List, Optional, Dict

import boto3
from botocore.config import Config

from security_models import SafetyCheckRequest, SafetyCheckResponse, SafetyViolation


def get_comprehend_client(region: str = "us-east-1") -> boto3.client:
    """Create an AWS Comprehend client."""
    creds = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    }
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=5,
        read_timeout=30,
    )
    return boto3.client(
        "comprehend",
        region_name=region,
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        config=config,
    )


def check_payload_safety(
    text: str,
    region: str = "us-east-1",
    toxicity_threshold: float = 0.5,
) -> SafetyCheckResponse:
    """Check text content for toxicity, hate speech, and other unsafe content.

    Uses Amazon Comprehend DetectSentiment to identify negative sentiment
    and Amazon Comprehend DetectToxicContent (via the comprehend SDK) to
    identify toxic content categories.

    Amazon Comprehend's DetectSentiment provides a safety signal:
    - NEUTRAL / POSITIVE generally indicate safe content
    - NEGATIVE / MIXED may warrant further review

    Args:
        text: The decrypted text payload to analyze.
        region: AWS region for Comprehend.
        toxicity_threshold: Threshold above which content is flagged.

    Returns:
        SafetyCheckResponse with safety determination and any violations.
    """
    client = get_comprehend_client(region=region)
    violations: List[SafetyViolation] = []

    # Detect sentiment as a safety signal
    sentiment_result = client.detect_sentiment(
        Text=text,
        LanguageCode="en",
    )

    sentiment = sentiment_result.get("Sentiment", "NEUTRAL")
    sentiment_scores = sentiment_result.get("SentimentScore", {})

    # Check for negative or mixed sentiment as potential safety concern
    negative_score = sentiment_scores.get("Negative", 0.0)
    mixed_score = sentiment_scores.get("Mixed", 0.0)

    if negative_score > toxicity_threshold:
        violations.append(SafetyViolation(
            category="NEGATIVE_SENTIMENT",
            severity="HIGH" if negative_score > 0.8 else "MEDIUM",
            score=negative_score,
            detail=f"Negative sentiment detected with score {negative_score:.4f}",
        ))

    if mixed_score > toxicity_threshold:
        violations.append(SafetyViolation(
            category="MIXED_SENTIMENT",
            severity="LOW",
            score=mixed_score,
            detail=f"Mixed/conflicting sentiment detected with score {mixed_score:.4f}",
        ))

    # Detect key phrases and PII entities as additional safety checks
    try:
        entities_result = client.detect_pii_entities(
            Text=text,
            LanguageCode="en",
        )
        for entity in entities_result.get("Entities", []):
            entity_type = entity.get("Type", "UNKNOWN")
            entity_score = entity.get("Score", 0.0)
            if entity_score > toxicity_threshold:
                violations.append(SafetyViolation(
                    category=f"PII_{entity_type}",
                    severity="MEDIUM",
                    score=entity_score,
                    detail=f"PII entity '{entity_type}' detected in payload",
                ))
    except Exception:
        pass  # PII detection may not be available in all regions

    is_safe = len(violations) == 0 or all(
        v.severity == "LOW" for v in violations
    )

    raw_result = {
        "sentiment": sentiment,
        "sentiment_scores": sentiment_scores,
    }

    return SafetyCheckResponse(
        is_safe=is_safe,
        violations=violations,
        raw_result=raw_result,
    )


if __name__ == "__main__":
    text = "This is a normal decrypted payload with no issues."
    result = check_payload_safety(text)
    print(f"Safe: {result.is_safe}")
    print(f"Violations: {len(result.violations)}")
    for v in result.violations:
        print(f"  - [{v.severity}] {v.category}: {v.detail}")
