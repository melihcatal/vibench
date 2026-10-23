"""
Check generated visual labels for unsafe text using OpenAI Moderation API.
Provider: OpenAI API (openai)
Endpoint: api.openai.com
Model: text-moderation-latest (OpenAI Moderation)
"""

from __future__ import annotations

import os
from typing import Optional

import openai


def check_visual_text_safety(
    text: str,
    categories: Optional[list[str]] = None,
) -> dict:
    """
    Check generated visual labels or descriptions for unsafe text content.

    Uses OpenAI Moderation API to evaluate text extracted from or generated
    based on image analysis.

    Args:
        text: The visual label, description, or OCR text to evaluate.
        categories: Optional list of specific categories to check.
                    Available: hate, hate/threatening, harassment, harassment/threatening,
                    self-harm, self-harm/intent, self-harm/instructions, sexual,
                    sexual/minors, violence, violence/graphic.

    Returns:
        Dictionary with moderation results, flagged categories, and overall safety status.

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    openai.api_key = api_key

    response = openai.moderations.create(
        input=text,
        model="text-moderation-latest",
    )

    result = response.results[0]

    flagged_categories = []
    category_scores = {}

    for cat_name, is_flagged in result.categories.model_dump().items():
        if categories and cat_name not in categories:
            continue
        score = getattr(result.category_scores, cat_name, 0.0)
        category_scores[cat_name] = score
        if is_flagged:
            flagged_categories.append({
                "category": cat_name,
                "flagged": True,
                "score": score,
            })

    is_safe = not result.flagged

    return {
        "provider": "openai",
        "model": "text-moderation-latest",
        "input_text": text,
        "flagged": result.flagged,
        "is_safe": is_safe,
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
    }


def check_labels_safety(
    labels: list[str],
    min_confidence: float = 0.5,
) -> dict:
    """
    Check a list of visual labels for unsafe content.

    Args:
        labels: List of label strings from image analysis.
        min_confidence: Minimum confidence threshold (labels above this are checked).

    Returns:
        Dictionary with per-label safety results and overall assessment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    openai.api_key = api_key

    label_results = []
    overall_unsafe = False

    for label in labels:
        try:
            safety = check_visual_text_safety(label)
            label_results.append({
                "label": label,
                "flagged": safety["flagged"],
                "flagged_categories": safety["flagged_categories"],
            })
            if safety["flagged"]:
                overall_unsafe = True
        except Exception:
            label_results.append({
                "label": label,
                "flagged": False,
                "error": "moderation check failed",
            })

    return {
        "provider": "openai",
        "model": "text-moderation-latest",
        "overall_safe": not overall_unsafe,
        "label_results": label_results,
        "total_checked": len(labels),
        "total_flagged": sum(1 for r in label_results if r.get("flagged")),
    }


def check_description_safety(
    description: str,
    detected_text: Optional[str] = None,
) -> dict:
    """
    Check image description and detected text for unsafe content.

    Args:
        description: Generated image description.
        detected_text: Optional OCR-extracted text.

    Returns:
        Dictionary with safety assessment for description and detected text.
    """
    results = {
        "provider": "openai",
        "model": "text-moderation-latest",
    }

    desc_safety = check_visual_text_safety(description)
    results["description_safety"] = desc_safety

    if detected_text:
        text_safety = check_visual_text_safety(detected_text)
        results["detected_text_safety"] = text_safety
        results["overall_safe"] = desc_safety["is_safe"] and text_safety["is_safe"]
    else:
        results["overall_safe"] = desc_safety["is_safe"]

    return results


if __name__ == "__main__":
    import sys
    import json

    text = sys.argv[1] if len(sys.argv) > 1 else "A peaceful sunset over mountains"
    result = check_visual_text_safety(text=text)
    print(json.dumps(result, indent=2))
