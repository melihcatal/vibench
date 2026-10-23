"""
Check decrypted text payloads for unsafe content.

Uses AWS Comprehend (comprehend.amazonaws.com) with the boto3 SDK
to analyze decrypted plaintext for PII, toxic content, and other
sensitive or unsafe material patterns.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)

COMPEND_ENDPOINT = "comprehend.amazonaws.com"


@dataclass
class SafetyCheckResult:
    is_safe: bool
    pii_detected: bool
    toxic_detected: bool
    findings: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    provider: str = "aws_comprehend"


def get_comprehend_client(region: Optional[str] = None):
    """
    Initialize an AWS Comprehend boto3 client.

    Provider: AWS Comprehend (comprehend.amazonaws.com)
    """
    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    credentials = {}
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if access_key:
        credentials["aws_access_key_id"] = access_key
    if secret_key:
        credentials["aws_secret_access_key"] = secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=30,
    )

    return boto3.client(
        "comprehend",
        region_name=resolved_region,
        config=config,
        **credentials,
    )


def detect_pii(text: str, client=None) -> List[Dict[str, Any]]:
    """
    Detect PII entities in text using AWS Comprehend DetectPiiEntities.

    Provider: AWS Comprehend (comprehend.amazonaws.com)
    API: comprehend.detect_pii_entities

    Args:
        text: The text payload to analyze.
        client: Optional pre-initialized Comprehend client.

    Returns:
        List of detected PII entity dictionaries.
    """
    if client is None:
        client = get_comprehend_client()

    if not text or len(text.strip()) == 0:
        return []

    truncated_text = text[:4999]

    logger.info("Calling AWS Comprehend DetectPiiEntities")

    response = client.detect_pii_entities(
        Text=truncated_text,
        LanguageCode="en",
    )

    entities = response.get("Entities", [])
    return [
        {
            "type": entity.get("Type"),
            "score": entity.get("Score", 0.0),
            "begin_offset": entity.get("BeginOffset"),
            "end_offset": entity.get("EndOffset"),
        }
        for entity in entities
    ]


def detect_sentiment(text: str, client=None) -> Dict[str, Any]:
    """
    Analyze sentiment of text using AWS Comprehend DetectSentiment.

    Provider: AWS Comprehend (comprehend.amazonaws.com)
    API: comprehend.detect_sentiment

    Args:
        text: The text payload to analyze.
        client: Optional pre-initialized Comprehend client.

    Returns:
        Dictionary with sentiment scores.
    """
    if client is None:
        client = get_comprehend_client()

    if not text or len(text.strip()) == 0:
        return {"sentiment": "NEUTRAL", "scores": {}}

    truncated_text = text[:4999]

    response = client.detect_sentiment(
        Text=truncated_text,
        LanguageCode="en",
    )

    return {
        "sentiment": response.get("Sentiment", "NEUTRAL"),
        "scores": response.get("SentimentScore", {}),
    }


def check_payload_safety(
    plaintext: str,
    pii_threshold: float = 0.7,
    toxicity_threshold: float = 0.8,
    region: Optional[str] = None,
) -> SafetyCheckResult:
    """
    Check a decrypted text payload for unsafe content.

    Provider: AWS Comprehend (comprehend.amazonaws.com)
    APIs: comprehend.detect_pii_entities, comprehend.detect_sentiment

    Args:
        plaintext: The decrypted plaintext to analyze.
        pii_threshold: Confidence threshold for PII flagging (default: 0.7).
        toxicity_threshold: Confidence threshold for toxic content (default: 0.8).
        region: Optional AWS region override.

    Returns:
        SafetyCheckResult with safety assessment.
    """
    client = get_comprehend_client(region=region)
    findings = []
    confidence_scores = {}

    pii_entities = detect_pii(plaintext, client)
    pii_detected = False

    for entity in pii_entities:
        if entity["score"] >= pii_threshold:
            pii_detected = True
            findings.append({
                "type": "pii",
                "category": entity["type"],
                "confidence": entity["score"],
                "offsets": {
                    "begin": entity["begin_offset"],
                    "end": entity["end_offset"],
                },
            })
            confidence_scores[f"pii_{entity['type']}"] = entity["score"]

    sentiment = detect_sentiment(plaintext, client)
    toxic_detected = False

    negative_score = sentiment.get("scores", {}).get("Negative", 0.0)
    if negative_score >= toxicity_threshold:
        toxic_detected = True
        findings.append({
            "type": "toxicity",
            "category": "negative_sentiment",
            "confidence": negative_score,
        })
        confidence_scores["negative_sentiment"] = negative_score

    is_safe = not pii_detected and not toxic_detected

    return SafetyCheckResult(
        is_safe=is_safe,
        pii_detected=pii_detected,
        toxic_detected=toxic_detected,
        findings=findings,
        confidence_scores=confidence_scores,
        provider="aws_comprehend",
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_text = os.environ.get("PAYLOAD_SAFETY_TEST_TEXT", "")
    if sample_text:
        result = check_payload_safety(sample_text)
        print(f"Safe: {result.is_safe}")
        print(f"PII detected: {result.pii_detected}")
        print(f"Findings: {result.findings}")
    else:
        print("Set PAYLOAD_SAFETY_TEST_TEXT environment variable to test.")
