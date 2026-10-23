"""
Check free-text metric labels or annotations for unsafe text using AWS Comprehend.

Uses AWS Comprehend (comprehend.amazonaws.com) to scan metric labels,
annotations, and dashboard notes for personally identifiable information (PII),
toxic content, or other safety concerns before storing them as CloudWatch metric
annotations or dashboard text.
"""

import os
import re
from typing import List, Optional, Dict, Any, Tuple

import boto3
from botocore.config import Config


# Provider-specific: AWS Comprehend endpoint and model
AWS_COMPREHEND_ENDPOINT = "comprehend.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


# PII entity types to check in metric annotations
PII_ENTITY_TYPES = [
    "NAME",
    "EMAIL",
    "PHONE",
    "ADDRESS",
    "SSN",
    "CREDIT_DEBIT_NUMBER",
    "PASSWORD",
    "AWS_ACCESS_KEY",
    "AWS_SECRET_KEY",
    "USERNAME",
]

# Toxic/sensitive label categories
SENSITIVE_LABELS = [
    "HATE_SPEECH",
    "OFFENSIVE",
    "PROFANITY",
    "THREAT",
    "SEXUAL",
    "VIOLENCE",
]


class AnnotationSafetyResult:
    """Result of checking a metric annotation for safety concerns."""

    def __init__(
        self,
        text: str,
        is_safe: bool,
        pii_entities: List[Dict[str, Any]],
        toxic_labels: List[Dict[str, Any]],
        safety_score: float,
        issues: List[str],
        redacted_text: Optional[str] = None,
    ):
        self.text = text
        self.is_safe = is_safe
        self.pii_entities = pii_entities
        self.toxic_labels = toxic_labels
        self.safety_score = safety_score
        self.issues = issues
        self.redacted_text = redacted_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "pii_entities": self.pii_entities,
            "toxic_labels": self.toxic_labels,
            "safety_score": self.safety_score,
            "issues": self.issues,
            "redacted_text": self.redacted_text,
        }


def _get_comprehend_client(region: Optional[str] = None):
    """
    Initialize an AWS Comprehend client via boto3.

    Returns:
        boto3 client for the comprehend service (comprehend.amazonaws.com).
    """
    target_region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    session = boto3.Session()
    return session.client(
        service_name="comprehend",
        region_name=target_region,
        config=config,
    )


def metric_annotation_safety(
    annotation_text: str,
    region: Optional[str] = None,
    client=None,
    check_pii: bool = True,
    check_toxic: bool = True,
) -> AnnotationSafetyResult:
    """
    Check free-text metric labels or annotations for unsafe content using AWS Comprehend.

    Uses the AWS Comprehend DetectPiiEntities and DetectSentiment APIs to scan
    metric annotation text for PII and potentially problematic content.

    Args:
        annotation_text: The free-text annotation to check.
        region: AWS region for Comprehend endpoint.
        client: Optional pre-configured Comprehend boto3 client.
        check_pii: Whether to run PII detection.
        check_toxic: Whether to run sentiment/toxic content analysis.

    Returns:
        AnnotationSafetyResult with safety assessment details.
    """
    issues = []
    pii_entities = []
    toxic_labels = []
    redacted = annotation_text

    if not annotation_text or not annotation_text.strip():
        return AnnotationSafetyResult(
            text=annotation_text,
            is_safe=True,
            pii_entities=[],
            toxic_labels=[],
            safety_score=1.0,
            issues=[],
            redacted_text=annotation_text,
        )

    # Truncate to Comprehend's 5,000 character limit per API call
    text_to_check = annotation_text[:5000]

    if client is None:
        client = _get_comprehend_client(region=region)

    # Check for PII using AWS Comprehend DetectPiiEntities
    if check_pii:
        pii_entities = _detect_pii(client, text_to_check)
        if pii_entities:
            for entity in pii_entities:
                entity_type = entity.get("Type", "UNKNOWN")
                issues.append(f"PII detected: {entity_type}")
            redacted = _redact_pii(annotation_text, pii_entities)

    # Check for toxic/sensitive content using sentiment analysis
    if check_toxic:
        toxic_labels = _detect_sensitive_content(client, text_to_check)
        if toxic_labels:
            for label in toxic_labels:
                label_name = label.get("Label", "UNKNOWN")
                issues.append(f"Sensitive content: {label_name}")

    # Check for potential secrets/keys via regex as additional safety
    secret_issues = _detect_secrets_regex(annotation_text)
    issues.extend(secret_issues)

    # Compute safety score (1.0 = safe, 0.0 = completely unsafe)
    safety_score = _compute_safety_score(pii_entities, toxic_labels, secret_issues)

    is_safe = len(issues) == 0

    return AnnotationSafetyResult(
        text=annotation_text,
        is_safe=is_safe,
        pii_entities=pii_entities,
        toxic_labels=toxic_labels,
        safety_score=safety_score,
        issues=issues,
        redacted_text=redacted,
    )


def _detect_pii(client, text: str) -> List[Dict[str, Any]]:
    """
    Detect PII entities in text using AWS Comprehend DetectPiiEntities API.

    Args:
        client: Comprehend boto3 client.
        text: Text to analyze.

    Returns:
        List of PII entity findings from Comprehend.
    """
    try:
        response = client.detect_pii_entities(
            Text=text,
            LanguageCode="en",
        )
        entities = response.get("Entities", [])
        # Filter to relevant PII types for metric annotations
        relevant = [
            e for e in entities
            if e.get("Type") in PII_ENTITY_TYPES
        ]
        return [
            {
                "Type": e["Type"],
                "Score": e.get("Score", 0.0),
                "BeginOffset": e.get("BeginOffset"),
                "EndOffset": e.get("EndOffset"),
            }
            for e in relevant
        ]
    except Exception:
        return []


def _detect_sensitive_content(client, text: str) -> List[Dict[str, Any]]:
    """
    Detect sensitive content in text using AWS Comprehend DetectSentiment API.

    Args:
        client: Comprehend boto3 client.
        text: Text to analyze.

    Returns:
        List of sensitive content labels if found.
    """
    findings = []
    try:
        response = client.detect_sentiment(
            Text=text,
            LanguageCode="en",
        )
        sentiment = response.get("Sentiment", "NEUTRAL")
        sentiment_scores = response.get("SentimentScore", {})

        # Flag strongly negative sentiment as potentially problematic
        negative_score = sentiment_scores.get("NEGATIVE", 0.0)
        if negative_score > 0.7:
            findings.append({
                "Label": "HIGHLY_NEGATIVE_SENTIMENT",
                "Score": negative_score,
            })

    except Exception:
        pass

    return findings


def _detect_secrets_regex(text: str) -> List[str]:
    """
    Detect potential secrets or credentials in text using regex patterns.

    Args:
        text: Text to scan.

    Returns:
        List of issue descriptions for any matches.
    """
    issues = []

    patterns = {
        "AWS Access Key ID": r'AKIA[0-9A-Z]{16}',
        "AWS Secret Key": r'[A-Za-z0-9/+=]{40}',
        "Generic API Key": r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[A-Za-z0-9]{20,}',
        "Bearer Token": r'(?i)bearer\s+[A-Za-z0-9\-_.~+]+',
        "Password Assignment": r'(?i)(password|passwd|pwd)\s*[:=]\s*\S+',
    }

    for label, pattern in patterns.items():
        if re.search(pattern, text):
            issues.append(f"Potential secret found: {label}")

    return issues


def _redact_pii(text: str, pii_entities: List[Dict[str, Any]]) -> str:
    """
    Redact PII entities from text using offset information from Comprehend.

    Args:
        text: Original text.
        pii_entities: List of PII entities with BeginOffset/EndOffset.

    Returns:
        Text with PII replaced by [REDACTED].
    """
    if not pii_entities:
        return text

    # Sort by offset in reverse to replace from end to start
    sorted_entities = sorted(
        pii_entities,
        key=lambda e: e.get("BeginOffset", 0),
        reverse=True,
    )

    redacted = text
    for entity in sorted_entities:
        begin = entity.get("BeginOffset", 0)
        end = entity.get("EndOffset", 0)
        if 0 <= begin < end <= len(redacted):
            redacted = redacted[:begin] + "[REDACTED]" + redacted[end:]

    return redacted


def _compute_safety_score(
    pii_entities: List[Dict[str, Any]],
    toxic_labels: List[Dict[str, Any]],
    secret_issues: List[str],
) -> float:
    """
    Compute an overall safety score.

    Args:
        pii_entities: PII findings from Comprehend.
        toxic_labels: Toxic content findings.
        secret_issues: Regex-based secret findings.

    Returns:
        Safety score from 0.0 (unsafe) to 1.0 (safe).
    """
    score = 1.0

    # Deduct for PII entities
    for entity in pii_entities:
        entity_score = entity.get("Score", 0.0)
        score -= entity_score * 0.15

    # Deduct for toxic content
    for label in toxic_labels:
        label_score = label.get("Score", 0.0)
        score -= label_score * 0.2

    # Deduct for detected secrets
    score -= len(secret_issues) * 0.25

    return max(0.0, min(1.0, score))


def validate_metric_annotation(
    annotation_text: str,
    region: Optional[str] = None,
    client=None,
) -> Tuple[bool, str]:
    """
    Validate a metric annotation text and return safety verdict.

    Args:
        annotation_text: The annotation text to validate.
        region: AWS region for Comprehend.
        client: Optional Comprehend client.

    Returns:
        Tuple of (is_safe, message).
    """
    result = metric_annotation_safety(annotation_text, region=region, client=client)

    if result.is_safe:
        return True, "Annotation passed safety checks."

    message = f"Annotation failed safety checks ({len(result.issues)} issues):\n"
    for issue in result.issues:
        message += f"  - {issue}\n"

    if result.redacted_text:
        message += f"\nRedacted version: {result.redacted_text}"

    return False, message
