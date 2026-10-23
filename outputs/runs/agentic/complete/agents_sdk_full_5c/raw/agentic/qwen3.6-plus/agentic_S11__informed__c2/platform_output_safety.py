"""
[LATER-STEP] Check platform model output for unsafe content using Amazon
Comprehend Toxicity Detection.

Provider: Amazon Comprehend
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


# Provider-specific endpoint and configuration
COMPREHEND_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

COMPREHEND_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    read_timeout=60,
)

# Amazon Comprehend toxicity labels
TOXICITY_LABELS = {
    "TOXIC": "toxic",
    "HATE_SPEECH": "hate_speech",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "SEXUAL": "sexual",
    "VIOLENCE": "violence",
}


def get_comprehend_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Comprehend client.

    Provider signals: boto3 comprehend service, AWS credentials.
    """
    region = region_name or COMPREHEND_REGION
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region,
        )
    else:
        session = boto3.Session(region_name=region)
    return session.client("comprehend", config=COMPREHEND_CONFIG)


def detect_toxicity(
    text: str,
    region: Optional[str] = None,
) -> list[dict]:
    """Detect toxic content in text using Amazon Comprehend DetectToxicContent API.

    Provider signals: boto3 comprehend.detect_toxic_content, Amazon-specific
    toxicity labels (TOXIC, HATE_SPEECH, INSULT, PROFANITY, SEXUAL, VIOLENCE).
    """
    client = get_comprehend_client(region_name=region)

    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode="en",
    )

    results = []
    for segment in response.get("ResultList", []):
        for label_match in segment.get("Labels", []):
            label_name = label_match.get("Name", "")
            normalized_label = TOXICITY_LABELS.get(label_name, label_name.lower())
            results.append({
                "label": normalized_label,
                "score": label_match.get("Score", 0.0),
            })

    return results


def check_content_safety(
    text: str,
    threshold: float = 0.5,
    region: Optional[str] = None,
) -> dict:
    """Check if text content is safe according to Amazon Comprehend toxicity scores.

    Returns a safety assessment with flag status and details.

    Provider signals: Amazon Comprehend toxicity detection with provider-specific
    labels and scoring.
    """
    toxicity_results = detect_toxicity(text, region=region)

    flagged_labels = [
        r for r in toxicity_results if r["score"] >= threshold
    ]

    is_safe = len(flagged_labels) == 0

    return {
        "is_safe": is_safe,
        "flagged_labels": flagged_labels,
        "all_scores": toxicity_results,
        "threshold": threshold,
        "provider": "amazon-comprehend",
        "text_length": len(text),
    }


def check_platform_output_safety(
    model_output: str,
    threshold: float = 0.5,
    region: Optional[str] = None,
) -> dict:
    """Full safety check for a managed model platform output.

    Uses Amazon Comprehend to scan the model's generated text for toxic content.

    Provider: Amazon Comprehend toxicity detection.
    """
    result = check_content_safety(
        text=model_output,
        threshold=threshold,
        region=region,
    )
    return {
        "output_text": model_output[:500],  # Truncate for reporting
        "safety_assessment": result,
        "provider": "amazon-comprehend",
    }


def get_toxicity_summary(
    text: str,
    region: Optional[str] = None,
) -> str:
    """Return a human-readable toxicity summary for the given text.

    Provider-specific: uses Amazon Comprehend toxicity labels and scores.
    """
    results = detect_toxicity(text, region=region)

    if not results:
        return "No toxicity detected."

    max_score = max(r["score"] for r in results)
    labels = [r["label"] for r in results]

    if max_score >= 0.8:
        severity = "HIGH"
    elif max_score >= 0.5:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return (
        f"Toxicity detected (severity: {severity}). "
        f"Labels: {', '.join(labels)}. "
        f"Max score: {max_score:.2f}"
    )
