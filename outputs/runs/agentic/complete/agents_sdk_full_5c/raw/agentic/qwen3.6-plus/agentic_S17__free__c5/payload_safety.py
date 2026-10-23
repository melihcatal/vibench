"""
payload_safety.py - Check decrypted text payloads for unsafe content using Google Cloud Natural Language API.

Provider: Google Cloud Natural Language API
Service endpoint: language.googleapis.com
Concrete model: Google Cloud Natural Language moderation / text classification
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from google.cloud import language_v1


@dataclass
class SafetyCheckResult:
    """Result of a payload safety check."""
    is_safe: bool
    categories: List[Dict[str, float]]
    sentiment_score: float
    sentiment_magnitude: float
    flagged_reasons: List[str]


@dataclass
class SafetyConfig:
    """Configuration for safety checking thresholds."""
    sentiment_threshold: float = -0.5
    max_category_confidence: float = 0.7
    blocked_categories: Optional[List[str]] = None


DEFAULT_BLOCKED_CATEGORIES = [
    "Armed Conflict",
    "Crime & Justice",
    "Health Conditions",
    "Adult",
    "Violence",
    "Hate Speech",
    "Self-Harm",
]


def classify_text_payload(
    text: str,
    max_categories: int = 10,
    config: Optional[dict] = None,
) -> List[Dict[str, float]]:
    """
    Classify the content of a text payload using Google Cloud Natural Language API.

    Uses the google-cloud-language client to classify text into content categories
    via the language.googleapis.com endpoint. This helps detect potentially
    unsafe content in decrypted payloads.

    Args:
        text: The decrypted text payload to classify.
        max_categories: Maximum number of categories to return.
        config: Optional client configuration overrides.

    Returns:
        List of category dictionaries with name and confidence scores.
    """
    client_kwargs = {}
    if config and config.get("credentials_path"):
        client_kwargs["client_options"] = {
            "credentials_file": config["credentials_path"]
        }

    client = language_v1.LanguageServiceClient(**client_kwargs)

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="en",
    )

    response = client.classify_text(
        request={"document": document}
    )

    categories = []
    for category in response.categories[:max_categories]:
        categories.append({
            "name": category.name,
            "confidence": category.confidence,
        })

    return categories


def analyze_sentiment(
    text: str,
    config: Optional[dict] = None,
) -> dict:
    """
    Analyze the sentiment of a text payload using Google Cloud Natural Language API.

    Uses language.googleapis.com to detect sentiment score (-1.0 to 1.0)
    and magnitude (0.0+) which helps flag negatively-toned content.

    Args:
        text: The text to analyze.
        config: Optional client configuration.

    Returns:
        Dictionary with sentiment score and magnitude.
    """
    client_kwargs = {}
    if config and config.get("credentials_path"):
        client_kwargs["client_options"] = {
            "credentials_file": config["credentials_path"]
        }

    client = language_v1.LanguageServiceClient(**client_kwargs)

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="en",
    )

    response = client.analyze_sentiment(
        request={"document": document}
    )

    return {
        "score": response.document_sentiment.score,
        "magnitude": response.document_sentiment.magnitude,
    }


def check_payload_safety(
    decrypted_text: str,
    safety_config: Optional[SafetyConfig] = None,
    gc_config: Optional[dict] = None,
) -> SafetyCheckResult:
    """
    Perform a comprehensive safety check on decrypted text.

    Combines content classification and sentiment analysis from
    Google Cloud Natural Language API to determine if a decrypted
    payload contains unsafe content.

    Args:
        decrypted_text: The decrypted plaintext to check.
        safety_config: Thresholds and blocked categories.
        gc_config: Google Cloud client configuration.

    Returns:
        SafetyCheckResult with safety determination and details.
    """
    if safety_config is None:
        safety_config = SafetyConfig()

    blocked = safety_config.blocked_categories or DEFAULT_BLOCKED_CATEGORIES
    flagged_reasons: List[str] = []

    categories = classify_text_payload(decrypted_text, config=gc_config)
    sentiment = analyze_sentiment(decrypted_text, config=gc_config)

    for cat in categories:
        if cat["confidence"] > safety_config.max_category_confidence:
            for blocked_cat in blocked:
                if blocked_cat.lower() in cat["name"].lower():
                    flagged_reasons.append(
                        f"Blocked category detected: {cat['name']} "
                        f"(confidence: {cat['confidence']:.2f})"
                    )

    if sentiment["score"] < safety_config.sentiment_threshold:
        flagged_reasons.append(
            f"Negative sentiment detected: score={sentiment['score']:.2f}"
        )

    is_safe = len(flagged_reasons) == 0

    return SafetyCheckResult(
        is_safe=is_safe,
        categories=categories,
        sentiment_score=sentiment["score"],
        sentiment_magnitude=sentiment["magnitude"],
        flagged_reasons=flagged_reasons,
    )


if __name__ == "__main__":
    text = os.environ.get("PAYLOAD_TEXT", "This is a sample decrypted text payload.")

    result = check_payload_safety(text)
    print(f"Safe: {result.is_safe}")
    print(f"Sentiment: {result.sentiment_score}")
    print(f"Categories: {result.categories}")
    if result.flagged_reasons:
        print("Flagged reasons:")
        for reason in result.flagged_reasons:
            print(f"  - {reason}")
