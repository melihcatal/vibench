"""
[LATER-STEP] Check extracted document text for unsafe content using Google Cloud
Natural Language API's content moderation and entity analysis capabilities.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import language_v1
from google.cloud.language_v1 import LanguageServiceClient

from document_client import GOOGLE_CLOUD_PROJECT


GOOGLE_CLOUD_NLP_ENDPOINT = "language.googleapis.com"
GOOGLE_CLOUD_NLP_MODEL = "builtin/stable"


class GoogleNLPClient:
    """Client wrapper for Google Cloud Natural Language API."""

    def __init__(
        self,
        project: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.client = LanguageServiceClient()

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment using Google Cloud Natural Language API.
        Uses the builtin/stable model for consistent sentiment scoring.
        """
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        response = self.client.analyze_sentiment(
            request={"document": document}
        )
        return {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        }

    def analyze_entities(self, text: str) -> list:
        """
        Extract entities using Google Cloud Natural Language API.
        Identifies persons, organizations, locations, events, etc.
        """
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        response = self.client.analyze_entities(
            request={"document": document}
        )
        entities = []
        for entity in response.entities:
            entities.append({
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": len(entity.mentions),
            })
        return entities

    def classify_text(self, text: str) -> list:
        """
        Classify text into content categories using Google Cloud Natural Language API.
        Returns categories with confidence scores.
        """
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        response = self.client.classify_text(
            request={"document": document}
        )
        categories = []
        for category in response.categories:
            categories.append({
                "name": category.name,
                "confidence": category.confidence,
            })
        return categories


def check_ocr_safety(
    ocr_text: str,
    sentiment_threshold: float = -0.5,
    flagged_categories: Optional[List[str]] = None,
    client: Optional[GoogleNLPClient] = None,
) -> Dict[str, Any]:
    """
    Check extracted OCR text for unsafe content using Google Cloud Natural
    Language API sentiment analysis, entity extraction, and text classification.

    Uses the builtin/stable model via language.googleapis.com for content moderation.

    Args:
        ocr_text: Plain text extracted from OCR.
        sentiment_threshold: Negative sentiment score below which to flag content.
        flagged_categories: List of category names that indicate unsafe content.
        client: Optional pre-configured GoogleNLPClient.

    Returns:
        Dictionary with safety analysis results including flags and reasons.
    """
    if client is None:
        client = GoogleNLPClient()

    if flagged_categories is None:
        flagged_categories = [
            "/Adult",
            "/Violence & Hate",
            "/Weapons & Explosives",
            "/Drugs & Substances",
            "/Sensitive Subjects",
        ]

    if not ocr_text.strip():
        return {
            "is_safe": True,
            "flags": [],
            "sentiment": {"score": 0.0, "magnitude": 0.0},
            "entities": [],
            "categories": [],
            "model": GOOGLE_CLOUD_NLP_MODEL,
        }

    safety_result = {
        "is_safe": True,
        "flags": [],
        "model": GOOGLE_CLOUD_NLP_MODEL,
    }

    # Analyze sentiment
    sentiment = client.analyze_sentiment(ocr_text)
    safety_result["sentiment"] = sentiment

    if sentiment["score"] < sentiment_threshold:
        safety_result["is_safe"] = False
        safety_result["flags"].append(
            f"Negative sentiment detected (score: {sentiment['score']})"
        )

    # Analyze entities for PII and sensitive data
    entities = client.analyze_entities(ocr_text)
    safety_result["entities"] = entities

    sensitive_entity_types = {"PERSON", "PHONE_NUMBER", "LOCATION", "ADDRESS"}
    sensitive_entities = [
        e for e in entities if e["type"] in sensitive_entity_types
    ]
    if sensitive_entities:
        safety_result["flags"].append(
            f"Sensitive entities detected: {len(sensitive_entities)} items"
        )
        safety_result["sensitive_entities"] = sensitive_entities

    # Classify text content
    categories = client.classify_text(ocr_text)
    safety_result["categories"] = categories

    for category in categories:
        for flagged in flagged_categories:
            if flagged.lower() in category["name"].lower():
                safety_result["is_safe"] = False
                safety_result["flags"].append(
                    f"Flagged category: {category['name']} "
                    f"(confidence: {category['confidence']:.2f})"
                )

    # Check for known unsafe patterns in OCR text
    unsafe_patterns = _check_unsafe_patterns(ocr_text)
    if unsafe_patterns:
        safety_result["is_safe"] = False
        safety_result["flags"].extend(unsafe_patterns)

    return safety_result


def _check_unsafe_patterns(text: str) -> List[str]:
    """Check text for known unsafe patterns common in document scanning."""
    flags = []
    text_lower = text.lower()

    pii_patterns = [
        ("ssn" in text_lower and any(c.isdigit() for c in text_lower.split("ssn")[-1][:15] if "ssn" in text_lower else ""),
         "Possible SSN detected"),
        ("credit card" in text_lower, "Credit card reference detected"),
        ("password" in text_lower and ":" in text_lower, "Possible password exposure"),
    ]

    for condition, message in pii_patterns:
        try:
            if condition:
                flags.append(message)
        except Exception:
            pass

    return flags


def batch_check_documents(
    documents: List[str],
    sentiment_threshold: float = -0.5,
) -> List[Dict[str, Any]]:
    """
    Check multiple OCR documents for safety using Google Cloud Natural Language API.
    
    Uses language.googleapis.com with the builtin/stable model.
    """
    client = GoogleNLPClient()
    results = []

    for doc_text in documents:
        result = check_ocr_safety(
            doc_text,
            sentiment_threshold=sentiment_threshold,
            client=client,
        )
        results.append(result)

    return results


if __name__ == "__main__":
    sample_text = """CONFIDENTIAL - Employee Record
SSN: 123-45-6789
Name: John Doe
This document contains sensitive personal information."""

    result = check_ocr_safety(sample_text)
    print(f"Safe: {result['is_safe']}")
    for flag in result['flags']:
        print(f"  FLAG: {flag}")
