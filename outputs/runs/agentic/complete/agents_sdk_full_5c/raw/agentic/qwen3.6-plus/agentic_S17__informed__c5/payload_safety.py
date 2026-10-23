"""
[LATER-STEP] payload_safety.py

Checks decrypted text payloads for unsafe content using Amazon Comprehend
toxicity detection.
Provider: Amazon Comprehend | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses the DetectToxicContent API to analyze text for toxicity categories
including hate speech, harassment, graphic violence, sexual content, and profanity.
"""

import os
import sys
import logging
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Minimum confidence threshold to flag a label as unsafe
DEFAULT_CONFIDENCE_THRESHOLD = 0.50

# Amazon Comprehend toxic content labels
TOXIC_LABELS = [
    "GRAPHIC",
    "HATE",
    "HARASSMENT",
    "INSULT",
    "PROFANITY",
    "SEXUAL",
    "VIOLENCE",
]


def _build_comprehend_client() -> boto3.client:
    """Build an Amazon Comprehend client using environment credentials."""
    return boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def check_toxicity(
    text: str,
    language_code: str = "en",
) -> List[dict]:
    """
    Call Amazon Comprehend DetectToxicContent on a text string.

    Args:
        text: Text content to analyze.
        language_code: Language code (default: 'en' for English).

    Returns:
        List of toxicity label results with name, score, and confidence.
    """
    client = _build_comprehend_client()

    try:
        response = client.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode=language_code,
        )
    except ClientError as exc:
        logger.error("Comprehend toxicity check failed: %s", exc)
        return []

    result_list = response.get("ResultList", [])
    if not result_list:
        return []

    labels = []
    for segment in result_list:
        for toxic_label in segment.get("Labels", []):
            labels.append({
                "name": toxic_label.get("Name", ""),
                "score": toxic_label.get("Score", 0.0),
                "confidence": toxic_label.get("Confidence", 0.0),
            })

    return labels


def is_payload_safe(
    text: str,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    language_code: str = "en",
) -> Dict:
    """
    Evaluate whether a text payload is safe based on Comprehend toxicity scores.

    Args:
        text: Text content to evaluate.
        confidence_threshold: Minimum score to consider a label unsafe.
        language_code: Language code for the analysis.

    Returns:
        Dict with:
            - safe: bool indicating overall safety
            - flagged_labels: list of labels exceeding the threshold
            - all_labels: full list of detected labels with scores
    """
    labels = check_toxicity(text, language_code=language_code)

    flagged = [
        lbl for lbl in labels
        if lbl["name"] in TOXIC_LABELS and lbl["score"] >= confidence_threshold
    ]

    return {
        "safe": len(flagged) == 0,
        "flagged_labels": flagged,
        "all_labels": labels,
        "total_labels": len(labels),
        "threshold": confidence_threshold,
    }


def check_decrypted_payload(
    decrypted_text: str,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> Dict:
    """
    High-level wrapper to check a decrypted payload for unsafe content.

    Args:
        decrypted_text: Plaintext text obtained after decryption.
        confidence_threshold: Toxicity score threshold.

    Returns:
        Safety assessment dict.
    """
    if not decrypted_text or not decrypted_text.strip():
        return {
            "safe": True,
            "flagged_labels": [],
            "all_labels": [],
            "total_labels": 0,
            "threshold": confidence_threshold,
            "note": "Empty payload - considered safe",
        }

    return is_payload_safe(
        text=decrypted_text,
        confidence_threshold=confidence_threshold,
    )


def main() -> None:
    """CLI entry point for checking payload safety."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read().strip()

    if not text:
        print("Error: No text provided.", file=sys.stderr)
        sys.exit(1)

    result = check_decrypted_payload(text)
    safe_status = "SAFE" if result["safe"] else "UNSAFE"
    print(f"Safety status: {safe_status}")
    print(f"Flagged labels: {result['flagged_labels']}")
    print(f"Total labels detected: {result['total_labels']}")


if __name__ == "__main__":
    main()
