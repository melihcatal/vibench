"""
ocr_safety.py - Check extracted document text for unsafe content
using OpenAI Moderation API.

Provider: OpenAI
Model: omni-moderation-latest (OpenAI Moderation model)
"""

from typing import Optional, Dict, Any

from openai import OpenAI
from openai import OpenAIError

from document_client import (
    DocumentClientConfig,
    get_openai_client,
)
from document_models import OcrTextResult


def check_ocr_text_safety(
    ocr_result: OcrTextResult,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Check extracted OCR text for unsafe content using OpenAI Moderation API.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        Dictionary with safety flags, category scores, and flagged status.
    """
    if client is None:
        client = get_openai_client()

    text = ocr_result.extracted_text
    if not text or not text.strip():
        return _empty_safety_result()

    try:
        moderation = client.moderations.create(
            input=text,
            model="omni-moderation-latest",
        )
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI moderation check failed: {e}") from e

    result = moderation.results[0]

    flagged = result.flagged
    categories = {}
    category_scores = {}

    if hasattr(result, "categories"):
        categories = {
            cat: getattr(result.categories, cat, False)
            for cat in dir(result.categories)
            if not cat.startswith("_") and not callable(getattr(result.categories, cat, None))
        }

    if hasattr(result, "category_scores"):
        category_scores = {
            cat: float(getattr(result.category_scores, cat, 0.0))
            for cat in dir(result.category_scores)
            if not cat.startswith("_") and not callable(getattr(result.category_scores, cat, None))
        }

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "text_length": len(text),
        "model_id": "omni-moderation-latest",
    }


def check_ocr_lines_safety(
    ocr_result: OcrTextResult,
    client: Optional[OpenAI] = None,
) -> list:
    """
    Check each OCR line individually for unsafe content.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        List of safety results for each line.
    """
    if client is None:
        client = get_openai_client()

    lines = ocr_result.lines if ocr_result.lines else []
    results = []

    for idx, line in enumerate(lines):
        text = line.get("text", "")
        if not text or not text.strip():
            results.append({
                "line_index": idx,
                "text": text,
                "flagged": False,
                "categories": {},
                "category_scores": {},
            })
            continue

        try:
            moderation = client.moderations.create(
                input=text,
                model="omni-moderation-latest",
            )
        except OpenAIError as e:
            raise RuntimeError(f"OpenAI line moderation failed at line {idx}: {e}") from e

        result = moderation.results[0]
        flagged = result.flagged

        categories = {}
        category_scores = {}

        if hasattr(result, "categories"):
            categories = {
                cat: getattr(result.categories, cat, False)
                for cat in dir(result.categories)
                if not cat.startswith("_") and not callable(getattr(result.categories, cat, None))
            }

        if hasattr(result, "category_scores"):
            category_scores = {
                cat: float(getattr(result.category_scores, cat, 0.0))
                for cat in dir(result.category_scores)
                if not cat.startswith("_") and not callable(getattr(result.category_scores, cat, None))
            }

        results.append({
            "line_index": idx,
            "text": text,
            "flagged": flagged,
            "categories": categories,
            "category_scores": category_scores,
            "bounding_box": line.get("bounding_box"),
        })

    return results


def _empty_safety_result() -> Dict[str, Any]:
    """Return a default empty safety result."""
    return {
        "flagged": False,
        "categories": {},
        "category_scores": {},
        "text_length": 0,
        "model_id": "omni-moderation-latest",
    }


def summarize_safety_flags(
    safety_results: list,
) -> Dict[str, Any]:
    """
    Summarize safety check results across multiple checks.

    Args:
        safety_results: List of safety result dictionaries.

    Returns:
        Summary with total flagged count and highest risk categories.
    """
    total_flagged = sum(1 for r in safety_results if r.get("flagged", False))
    total_checks = len(safety_results)

    # Aggregate highest category scores
    max_scores: Dict[str, float] = {}
    for result in safety_results:
        for cat, score in result.get("category_scores", {}).items():
            if cat not in max_scores or score > max_scores[cat]:
                max_scores[cat] = score

    return {
        "total_checks": total_checks,
        "total_flagged": total_flagged,
        "clean_count": total_checks - total_flagged,
        "max_category_scores": max_scores,
        "overall_safe": total_flagged == 0,
    }
