"""
Moderate vendor notes or memo fields using OpenAI Moderation API.

Checks vendor-provided text fields (notes, memos, descriptions) for potentially
unsafe content using OpenAI's moderation endpoint before storing or displaying.

Provider: OpenAI
Model: text-moderation-latest
SDK: openai
API: https://api.openai.com/v1/moderations
"""

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODERATION_MODEL = "text-moderation-latest"


@dataclass
class ModerationResult:
    """Result of text moderation check."""
    text: str
    flagged: bool
    categories: dict[str, bool]
    category_scores: dict[str, float]
    is_safe: bool


def moderate_vendor_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = MODERATION_MODEL,
) -> ModerationResult:
    """
    Check vendor notes or memo text for unsafe content using OpenAI Moderation API.

    Evaluates text against OpenAI's moderation categories including:
    - hate, hate/threatening
    - self-harm, self-harm/intent, self-harm/instructions
    - sexual, sexual/minors
    - violence, violence/graphic
    - harassment, harassment/threatening
    - illicit, illicit/violent

    Args:
        text: Vendor note, memo, or description text to moderate.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI moderation model. Defaults to text-moderation-latest.

    Returns:
        ModerationResult with flag status and category details.

    Raises:
        ValueError: If OpenAI API key is not provided.
        openai.OpenAIError: If the OpenAI API call fails.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=key)

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result = response.results[0]

    categories = {}
    category_scores = {}
    if hasattr(result, 'categories') and result.categories:
        categories = {
            cat: getattr(result.categories, cat, False)
            for cat in dir(result.categories)
            if not cat.startswith('_') and isinstance(getattr(result.categories, cat, None), bool)
        }
    if hasattr(result, 'category_scores') and result.category_scores:
        category_scores = {
            cat: getattr(result.category_scores, cat, 0.0)
            for cat in dir(result.category_scores)
            if not cat.startswith('_') and isinstance(getattr(result.category_scores, cat, None), (int, float))
        }

    return ModerationResult(
        text=text,
        flagged=result.flagged,
        categories=categories,
        category_scores=category_scores,
        is_safe=not result.flagged,
    )


def moderate_vendor_notes(
    vendor_notes: dict[str, str],
    api_key: Optional[str] = None,
    model: str = MODERATION_MODEL,
) -> dict[str, ModerationResult]:
    """
    Moderate multiple vendor note fields in batch.

    Args:
        vendor_notes: Dictionary mapping field names to text values.
                      e.g., {"memo": "...", "description": "...", "notes": "..."}
        api_key: OpenAI API key.
        model: OpenAI moderation model.

    Returns:
        Dictionary mapping field names to their ModerationResult.
    """
    results = {}
    for field_name, text in vendor_notes.items():
        if text and text.strip():
            results[field_name] = moderate_vendor_text(
                text=text,
                api_key=api_key,
                model=model,
            )
        else:
            results[field_name] = ModerationResult(
                text=text or "",
                flagged=False,
                categories={},
                category_scores={},
                is_safe=True,
            )
    return results


def is_vendor_text_safe(
    text: str,
    api_key: Optional[str] = None,
    model: str = MODERATION_MODEL,
) -> bool:
    """
    Quick check if vendor text is safe for storage/display.

    Args:
        text: Vendor note or memo text.
        api_key: OpenAI API key.
        model: OpenAI moderation model.

    Returns:
        True if text is safe (not flagged), False otherwise.
    """
    result = moderate_vendor_text(text, api_key=api_key, model=model)
    return result.is_safe


def format_moderation_report(result: ModerationResult) -> dict:
    """
    Format moderation result into a structured report.

    Args:
        result: ModerationResult from moderation check.

    Returns:
        Dictionary with formatted moderation report.
    """
    return {
        "flagged": result.flagged,
        "is_safe": result.is_safe,
        "categories": result.categories,
        "highest_score_category": max(
            result.category_scores.items(),
            key=lambda x: x[1],
            default=("none", 0.0),
        )[0],
    }
