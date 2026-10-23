"""
Check user-generated document fields for unsafe content using Amazon Comprehend.
Connects to the Amazon Comprehend hosted text analysis service for toxicity
and content moderation detection.
"""

import os
import json
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Threshold scores above which content is flagged
TOXICITY_THRESHOLD = 0.75


def _get_comprehend_client():
    """Create and return a boto3 comprehend client for Amazon Comprehend."""
    return boto3.client(
        "comprehend",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Check a single text string for toxicity using Amazon Comprehend DetectToxicContent.

    Args:
        text: The user-generated text to analyze.

    Returns:
        Dict with keys:
          - 'is_safe' (bool): True if no toxicity above threshold detected.
          - 'toxic_labels' (list): Labels of detected toxic categories.
          - 'toxic_scores' (dict): Per-label confidence scores.
          - 'details' (list): Raw per-segment results from Comprehend.
    """
    if not text or not text.strip():
        return {"is_safe": True, "toxic_labels": [], "toxic_scores": {}, "details": []}

    client = _get_comprehend_client()

    try:
        response = client.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode="en",
        )
    except ClientError as e:
        return {
            "is_safe": False,
            "toxic_labels": ["error"],
            "toxic_scores": {"error": 1.0},
            "details": [{"error": str(e)}],
        }

    toxic_labels = []
    toxic_scores: Dict[str, float] = {}
    details = []

    for result in response.get("ResultList", []):
        for label in result.get("Labels", []):
            name = label.get("Name", "")
            score = label.get("Score", 0.0)
            toxic_scores[name] = score
            if score >= TOXICITY_THRESHOLD:
                toxic_labels.append(name)

        details.append(result)

    is_safe = len(toxic_labels) == 0

    return {
        "is_safe": is_safe,
        "toxic_labels": toxic_labels,
        "toxic_scores": toxic_scores,
        "details": details,
    }


def check_documents_safety(
    documents: List[Dict[str, Any]],
    text_field: str = "content",
) -> List[Dict[str, Any]]:
    """
    Check multiple document records for unsafe text content.

    Args:
        documents: List of document dicts containing user-generated fields.
        text_field: The field name in each document to analyze.

    Returns:
        List of safety check results, one per document.
    """
    results = []
    for doc in documents:
        text = doc.get(text_field, "")
        safety_result = check_text_safety(str(text))
        safety_result["document_id"] = doc.get("document_id", "unknown")
        results.append(safety_result)
    return results
