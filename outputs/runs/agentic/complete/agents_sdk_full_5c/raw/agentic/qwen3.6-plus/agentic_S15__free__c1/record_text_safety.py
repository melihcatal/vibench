"""
record_text_safety.py - Check user-generated document fields for unsafe content
using Google Cloud Perspective API.

Provider: Google Cloud Perspective API (commentanalyzer.googleapis.com)
"""

import os
from typing import Any, Dict, List

import requests

from database_models import DocumentRecord, extract_user_facing_fields

# Google Cloud Perspective API provider-specific configuration
GOOGLE_PERSPECTIVE_API_KEY = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY", "")
GOOGLE_PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

DEFAULT_SAFETY_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]

DEFAULT_THRESHOLD = 0.7


def check_text_safety(text: str, threshold: float = DEFAULT_THRESHOLD) -> Dict[str, Any]:
    """
    Check a text string for unsafe content using the Google Cloud Perspective API.
    Returns a dict with safety scores for each analyzed attribute.
    """
    if not text.strip():
        return {"safe": True, "scores": {}, "flagged_attributes": []}

    params = {"key": GOOGLE_PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in DEFAULT_SAFETY_ATTRIBUTES},
        "languages": ["en"],
    }

    response = requests.post(
        GOOGLE_PERSPECTIVE_API_URL,
        params=params,
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    result = response.json()

    attribute_scores = result.get("attributeScores", {})
    scores: Dict[str, float] = {}
    flagged: List[str] = []

    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged.append(attr_name)

    return {
        "safe": len(flagged) == 0,
        "scores": scores,
        "flagged_attributes": flagged,
    }


def check_record_safety(
    record: DocumentRecord, threshold: float = DEFAULT_THRESHOLD
) -> Dict[str, Any]:
    """
    Check all user-facing fields in a document record for unsafe content
    using Google Cloud Perspective API.
    Returns aggregated safety results.
    """
    user_fields = extract_user_facing_fields(record)
    overall_safe = True
    all_scores: Dict[str, Dict[str, float]] = {}
    all_flagged: Dict[str, List[str]] = {}

    for field_name, text in user_fields.items():
        field_result = check_text_safety(text, threshold=threshold)
        all_scores[field_name] = field_result["scores"]
        if field_result["flagged_attributes"]:
            overall_safe = False
            all_flagged[field_name] = field_result["flagged_attributes"]

    return {
        "doc_id": record.doc_id,
        "safe": overall_safe,
        "field_scores": all_scores,
        "flagged_fields": all_flagged,
    }


def check_records_safety(
    records: List[DocumentRecord], threshold: float = DEFAULT_THRESHOLD
) -> List[Dict[str, Any]]:
    """
    Check multiple document records for unsafe content.
    Returns a list of safety result dicts.
    """
    return [check_record_safety(r, threshold) for r in records]
