"""
Check secret labels and notes for unsafe text using OpenAI moderation API.

This module validates secret metadata (labels, descriptions, notes)
against safety policies using OpenAI's content moderation endpoint
at api.openai.com.
"""

import logging
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from security_models import SecretLabelCheckResult

logger = logging.getLogger(__name__)

OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the official SDK."""
    return OpenAI(
        api_key=__import__("os").environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_BASE,
    )


def check_label_safety(text: str) -> Dict[str, Any]:
    """
    Check if a label or note contains unsafe content using OpenAI moderation.

    Args:
        text: The label text or note to check.

    Returns:
        Dictionary with safety assessment from OpenAI moderation API.
    """
    try:
        client = _get_openai_client()

        moderation_response = client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text,
        )

        result = moderation_response.results[0] if moderation_response.results else None
        if not result:
            return {"flagged": False, "text": text}

        return {
            "flagged": result.flagged,
            "categories": {
                category: getattr(result.categories, category, False)
                for category in dir(result.categories)
                if not category.startswith("_") and not callable(getattr(result.categories, category))
            },
            "category_scores": {
                category: getattr(result.category_scores, category, 0)
                for category in dir(result.category_scores)
                if not category.startswith("_") and not callable(getattr(result.category_scores, category))
            },
            "text": text,
        }

    except openai.APIError as e:
        logger.error("OpenAI moderation API error: %s", str(e))
        return {"flagged": False, "error": str(e), "text": text}
    except Exception as e:
        logger.error("Error checking label safety: %s", str(e))
        return {"flagged": False, "error": str(e), "text": text}


def check_secret_label_safety(
    secret_name: str,
    labels: Dict[str, str],
    notes: Optional[str] = None,
) -> SecretLabelCheckResult:
    """
    Check all labels and notes on a secret for unsafe content.

    Uses OpenAI's text-moderation-latest model at api.openai.com.

    Args:
        secret_name: Name of the secret being checked.
        labels: Dictionary of label key-value pairs.
        notes: Optional additional notes text.

    Returns:
        SecretLabelCheckResult with safety assessment.
    """
    all_texts = []
    for key, value in labels.items():
        all_texts.append((f"label:{key}", f"{key}: {value}"))
    if notes:
        all_texts.append(("notes", notes))

    unsafe_fields = []
    unsafe_patterns = []

    for field_name, text in all_texts:
        check_result = check_label_safety(text)
        if check_result.get("flagged"):
            unsafe_fields.append(field_name)
            categories = check_result.get("categories", {})
            flagged_cats = [
                cat for cat, is_flagged in categories.items()
                if isinstance(is_flagged, bool) and is_flagged
            ]
            unsafe_patterns.extend(flagged_cats)

    is_safe = len(unsafe_fields) == 0

    return SecretLabelCheckResult(
        secret_name=secret_name,
        provider="openai-moderation",
        is_safe=is_safe,
        unsafe_fields=unsafe_fields,
        unsafe_patterns=unsafe_patterns,
    )
