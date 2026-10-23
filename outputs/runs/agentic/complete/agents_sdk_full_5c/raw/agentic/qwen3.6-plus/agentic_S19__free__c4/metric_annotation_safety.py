"""
Check free-text metric labels or annotations for unsafe text.

Uses Amazon Comprehend DetectSentiment and DetectPiiEntities APIs for content
safety analysis of metric annotations and dashboard notes.

Provider signals:
  - boto3 comprehend client (Amazon Comprehend)
  - Amazon Comprehend sentiment analysis and PII detection
  - AWS Comprehend environment / client
"""

from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.config import Config

from observability_client import AWS_REGION


COMPREHEND_LANG_CODE = "en"
SAFETY_SCORE_THRESHOLD = 0.75


class SafetyCheckResult:
    """Result of checking metric annotation text for safety concerns."""

    def __init__(
        self,
        text: str,
        is_safe: bool = True,
        sentiment: str = "NEUTRAL",
        sentiment_scores: Optional[Dict[str, float]] = None,
        pii_entities: Optional[List[Dict[str, Any]]] = None,
        risk_score: float = 0.0,
        flags: Optional[List[str]] = None,
    ):
        self.text = text
        self.is_safe = is_safe
        self.sentiment = sentiment
        self.sentiment_scores = sentiment_scores or {}
        self.pii_entities = pii_entities or []
        self.risk_score = risk_score
        self.flags = flags or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "sentiment": self.sentiment,
            "sentiment_scores": self.sentiment_scores,
            "pii_entity_count": len(self.pii_entities),
            "risk_score": self.risk_score,
            "flags": self.flags,
        }


def _create_comprehend_client():
    """Create a boto3 Amazon Comprehend client."""
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
    )
    session = boto3.Session(region_name=AWS_REGION)
    return session.client("comprehend", config=config)


def metric_annotation_safety(
    text: str,
    language_code: str = COMPREHEND_LANG_CODE,
    sentiment_threshold: float = SAFETY_SCORE_THRESHOLD,
) -> SafetyCheckResult:
    """
    Check free-text metric labels or annotations for unsafe content.

    Uses Amazon Comprehend DetectSentiment and DetectPiiEntities to analyze
    metric annotation text for negative sentiment and PII data leaks.

    Args:
        text: The metric annotation or label text to analyze
        language_code: Language code for Comprehend (default: 'en')
        sentiment_threshold: Score above which negative sentiment triggers a flag

    Returns:
        SafetyCheckResult with analysis details.
    """
    comprehend = _create_comprehend_client()

    result = SafetyCheckResult(text=text)

    truncated = text[:5000] if len(text) > 5000 else text

    sentiment_response = comprehend.detect_sentiment(
        Text=truncated,
        LanguageCode=language_code,
    )

    result.sentiment = sentiment_response.get("Sentiment", "NEUTRAL")
    result.sentiment_scores = sentiment_response.get("SentimentScore", {})

    pii_response = comprehend.detect_pii_entities(
        Text=truncated,
        LanguageCode=language_code,
    )

    result.pii_entities = pii_response.get("Entities", [])

    flags = []
    risk_score = 0.0

    negative_score = result.sentiment_scores.get("Negative", 0.0)
    if negative_score > sentiment_threshold:
        flags.append("negative_sentiment")
        risk_score += negative_score * 0.5

    if result.pii_entities:
        flags.append("pii_detected")
        risk_score += min(len(result.pii_entities) * 0.2, 0.5)

    for entity in result.pii_entities:
        entity_type = entity.get("Type", "")
        if entity_type in ["SECRET_ACCESS_KEY", "PASSWORD", "CREDIT_DEBIT_NUMBER"]:
            flags.append(f"critical_pii:{entity_type}")
            risk_score += 0.3

    mixed_score = result.sentiment_scores.get("Mixed", 0.0)
    if mixed_score > 0.8:
        flags.append("mixed_sentiment")

    risk_score = min(risk_score, 1.0)
    result.risk_score = risk_score
    result.flags = flags
    result.is_safe = risk_score < 0.5

    return result


def batch_check_annotations(
    texts: List[str],
    language_code: str = COMPREHEND_LANG_CODE,
) -> List[SafetyCheckResult]:
    """
    Batch check multiple metric annotations for safety.

    Uses Amazon Comprehend BatchDetectSentiment for efficiency.

    Args:
        texts: List of annotation texts to check
        language_code: Language code

    Returns:
        List of SafetyCheckResult objects.
    """
    comprehend = _create_comprehend_client()

    truncated = [t[:5000] if len(t) > 5000 else t for t in texts]

    results = []
    for text in truncated:
        result = metric_annotation_safety(text, language_code)
        results.append(result)

    return results
