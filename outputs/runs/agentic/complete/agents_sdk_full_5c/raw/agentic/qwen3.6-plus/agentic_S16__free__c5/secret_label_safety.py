"""
secret_label_safety.py - Check secret labels and notes for unsafe text.

Uses OpenAI moderation API to analyze secret labels, descriptions, and notes
for potentially unsafe content such as hardcoded credentials, PII, or
inappropriate text that should not appear in secret metadata.

Provider: OpenAI Moderation API (api.openai.com)
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

import openai
from openai import OpenAI

from security_models import SafetyCheckResult

logger = logging.getLogger(__name__)

# Provider-specific OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def get_openai_client() -> Optional[OpenAI]:
    """Create an OpenAI client for the moderation API."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY environment variable not set")
        return None
    client = OpenAI(api_key=OPENAI_API_KEY)
    return client


# Local pattern-based safety checks as a first pass
UNSAFE_PATTERNS = [
    "password=",
    "passwd=",
    "api_key=",
    "apikey=",
    "secret_key=",
    "access_token=",
    "aws_secret",
    "private_key",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN DSA PRIVATE KEY",
    "BEGIN EC PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PGP PRIVATE KEY",
    "sk_live_",
    "sk_test_",
    "ghp_",
    "xoxb-",
    "xoxp-",
]


def check_local_patterns(text: str) -> List[str]:
    """
    Check text against known unsafe patterns for embedded secrets.

    Returns a list of matched unsafe patterns found in the text.
    """
    text_lower = text.lower()
    found = []
    for pattern in UNSAFE_PATTERNS:
        if pattern.lower() in text_lower:
            found.append(pattern)
    return found


def check_label_safety(
    secret_id: str,
    text_to_check: str,
) -> SafetyCheckResult:
    """
    Check secret labels and notes for unsafe content using OpenAI Moderation API.

    Performs local pattern matching first, then uses the OpenAI moderation
    endpoint for content analysis.

    Args:
        secret_id: The identifier of the secret being checked.
        text_to_check: The label, description, or notes text to analyze.

    Returns:
        SafetyCheckResult with safety assessment details.
    """
    flagged_terms = check_local_patterns(text_to_check)

    # Use OpenAI moderation API for content analysis
    client = get_openai_client()
    moderation_result = None
    api_confidence = 0.0

    if client and text_to_check.strip():
        try:
            moderation = client.moderations.create(
                model=OPENAI_MODERATION_MODEL,
                input=text_to_check,
            )
            moderation_result = moderation.results[0] if moderation.results else None
            if moderation_result:
                api_confidence = float(
                    max(moderation_result.category_scores.values())
                    if moderation_result.category_scores
                    else 0.0
                )
                if moderation_result.flagged:
                    for category, flagged in moderation_result.categories.model_dump().items():
                        if flagged:
                            flagged_terms.append(f"openai:{category}")
        except Exception as e:
            logger.warning("OpenAI moderation API error: %s", e)

    is_safe = len(flagged_terms) == 0 and (moderation_result is None or not moderation_result.flagged)

    explanation_parts = []
    if flagged_terms:
        explanation_parts.append(f"Flagged patterns/terms: {', '.join(flagged_terms)}")
    if moderation_result and moderation_result.flagged:
        explanation_parts.append("OpenAI moderation API flagged this content")
    if not explanation_parts:
        explanation_parts.append("No unsafe content detected")

    return SafetyCheckResult(
        secret_id=secret_id,
        checked_text=text_to_check,
        is_safe=is_safe,
        flagged_terms=flagged_terms,
        confidence=api_confidence if api_confidence > 0 else (1.0 if is_safe else 0.5),
        explanation="; ".join(explanation_parts),
    )


def check_secret_labels(
    secret_id: str,
    labels: List[str],
    description: str = "",
) -> Dict[str, SafetyCheckResult]:
    """
    Check all labels and description of a secret for unsafe content.

    Args:
        secret_id: The identifier of the secret.
        labels: List of label strings to check.
        description: Optional secret description to check.

    Returns:
        Dictionary mapping label/description name to SafetyCheckResult.
    """
    results = {}
    for label in labels:
        result = check_label_safety(secret_id, label)
        results[f"label:{label}"] = result

    if description:
        result = check_label_safety(secret_id, description)
        results["description"] = result

    return results


def get_safety_summary(results: Dict[str, SafetyCheckResult]) -> Dict[str, object]:
    """
    Generate a summary of all safety check results.
    """
    total = len(results)
    safe_count = sum(1 for r in results.values() if r.is_safe)
    unsafe_items = [k for k, r in results.items() if not r.is_safe]

    return {
        "total_checked": total,
        "safe_count": safe_count,
        "unsafe_count": total - safe_count,
        "unsafe_items": unsafe_items,
        "overall_safe": safe_count == total,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_labels = ["prod-db-password", "contains api_key=abc123", "normal-label"]
    results = check_secret_labels("test-secret", test_labels)
    for name, result in results.items():
        status = "SAFE" if result.is_safe else "UNSAFE"
        print(f"[{status}] {name}: {result.explanation}")
