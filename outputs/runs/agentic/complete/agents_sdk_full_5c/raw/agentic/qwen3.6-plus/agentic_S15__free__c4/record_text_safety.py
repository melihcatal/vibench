"""
Check user-generated document fields for unsafe content using OpenAI Moderation API.
Uses the OpenAI text moderation model for content safety screening.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import openai
from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "text-moderation-latest"

UNSAFE_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client configured with the API key from environment."""
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise EnvironmentError(f"Environment variable {OPENAI_API_KEY_ENV} is not set.")
    return OpenAI(api_key=api_key)


def check_text_safety(
    text: str,
    model: str = OPENAI_MODERATION_MODEL,
    client: Optional[OpenAI] = None,
) -> dict[str, Any]:
    """
    Check a single text string for unsafe content using OpenAI Moderation API.
    
    Args:
        text: The text content to evaluate for safety.
        model: The OpenAI moderation model identifier (default: text-moderation-latest).
        client: Optional pre-configured OpenAI client instance.
    
    Returns:
        A dict with flagged status, category results, and overall safety verdict.
    """
    if client is None:
        client = _get_openai_client()

    moderation_result = client.moderations.create(
        input=text,
        model=model,
    )

    result_obj = moderation_result.results[0]
    categories = {}
    category_scores = {}

    for cat in UNSAFE_CATEGORIES:
        flagged = getattr(result_obj.categories, cat.replace("/", "_"), False)
        score = getattr(result_obj.category_scores, cat.replace("/", "_"), 0.0)
        categories[cat] = bool(flagged)
        category_scores[cat] = float(score)

    return {
        "flagged": bool(result_obj.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "is_safe": not result_obj.flagged,
    }


def check_document_fields_safety(
    document: dict[str, Any],
    fields_to_check: Optional[list[str]] = None,
    model: str = OPENAI_MODERATION_MODEL,
    client: Optional[OpenAI] = None,
) -> dict[str, Any]:
    """
    Check user-generated fields within a document record for unsafe content.
    
    Args:
        document: A document record dict with a 'content' sub-dict.
        fields_to_check: Optional list of field names within 'content' to check.
                         If None, all string-valued fields are checked.
        model: The OpenAI moderation model identifier.
        client: Optional pre-configured OpenAI client instance.
    
    Returns:
        A dict with per-field safety results and an overall document safety verdict.
    """
    if client is None:
        client = _get_openai_client()

    content = document.get("content", {})
    texts_to_check: list[tuple[str, str]] = []

    if fields_to_check:
        for field_name in fields_to_check:
            value = content.get(field_name)
            if isinstance(value, str) and value.strip():
                texts_to_check.append((field_name, value))
    else:
        for field_name, value in content.items():
            if isinstance(value, str) and value.strip():
                texts_to_check.append((field_name, value))

    if not texts_to_check:
        return {
            "doc_id": document.get("doc_id"),
            "is_safe": True,
            "field_results": {},
            "any_flagged": False,
        }

    # Check each field individually for granular results
    field_results: dict[str, dict[str, Any]] = {}
    any_flagged = False

    for field_name, text in texts_to_check:
        safety_result = check_text_safety(text, model=model, client=client)
        field_results[field_name] = safety_result
        if safety_result["flagged"]:
            any_flagged = True

    return {
        "doc_id": document.get("doc_id"),
        "is_safe": not any_flagged,
        "field_results": field_results,
        "any_flagged": any_flagged,
        "flagged_fields": [
            fname for fname, res in field_results.items() if res["flagged"]
        ],
    }


def batch_check_safety(
    texts: list[str],
    model: str = OPENAI_MODERATION_MODEL,
    client: Optional[OpenAI] = None,
) -> list[dict[str, Any]]:
    """
    Check a batch of text strings for unsafe content using OpenAI Moderation API.
    
    Args:
        texts: A list of text strings to evaluate.
        model: The OpenAI moderation model identifier.
        client: Optional pre-configured OpenAI client instance.
    
    Returns:
        A list of safety result dicts, one per input text.
    """
    if client is None:
        client = _get_openai_client()

    moderation_result = client.moderations.create(
        input=texts,
        model=model,
    )

    results = []
    for i, result_obj in enumerate(moderation_result.results):
        categories = {}
        category_scores = {}
        for cat in UNSAFE_CATEGORIES:
            flagged = getattr(result_obj.categories, cat.replace("/", "_"), False)
            score = getattr(result_obj.category_scores, cat.replace("/", "_"), 0.0)
            categories[cat] = bool(flagged)
            category_scores[cat] = float(score)

        results.append({
            "input_index": i,
            "flagged": bool(result_obj.flagged),
            "categories": categories,
            "category_scores": category_scores,
            "is_safe": not result_obj.flagged,
        })

    return results


if __name__ == "__main__":
    sample_doc = {
        "doc_id": "user-content-001",
        "content": {
            "title": "My Post",
            "body": "This is a completely safe and normal text.",
            "comment": "Another benign comment.",
        },
    }
    result = check_document_fields_safety(sample_doc)
    print(result)
