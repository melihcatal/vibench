"""
Check free-text metric labels or annotations for unsafe text.

Provider: OpenAI Moderation API (openai)
Uses openai OpenAI client and api.openai.com with text-moderation-latest model
for content safety checks on metric annotations and labels.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import openai

from observability_models import MetricAnnotation


def check_annotation_safety(
    annotation: MetricAnnotation,
    openai_api_key: Optional[str] = None,
    moderation_model: str = "text-moderation-latest",
) -> Dict[str, Any]:
    """
    Check a metric annotation for unsafe or inappropriate text using OpenAI Moderation API.

    Uses the OpenAI text-moderation-latest model via api.openai.com to scan
    annotation titles and content for policy-violating content.

    Args:
        annotation: MetricAnnotation with title and content to check.
        openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var).
        moderation_model: OpenAI moderation model, default text-moderation-latest.

    Returns:
        Dict with flagged status, categories, and safety score.
    """
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return {
            "safe": True,
            "flagged": False,
            "categories": {},
            "message": "No OpenAI API key provided; skipping moderation check.",
        }

    # Combine title and content for moderation
    full_text = f"{annotation.title}\n{annotation.content}"

    try:
        client = openai.OpenAI(api_key=api_key)
        moderation_response = client.moderations.create(
            input=full_text,
            model=moderation_model,
        )

        result = moderation_response.results[0] if moderation_response.results else None
        if result is None:
            return {
                "safe": True,
                "flagged": False,
                "categories": {},
                "message": "Empty moderation result.",
            }

        categories = {}
        for cat_name, cat_flagged in result.categories.model_dump().items():
            if cat_flagged:
                categories[cat_name] = result.category_scores.model_dump().get(cat_name, 0.0)

        return {
            "safe": not result.flagged,
            "flagged": result.flagged,
            "categories": categories,
            "category_scores": result.category_scores.model_dump(),
            "message": "Content is safe." if not result.flagged else "Content flagged for review.",
        }
    except openai.AuthenticationError:
        return {
            "safe": False,
            "flagged": True,
            "categories": {},
            "message": "OpenAI authentication failed. Check API key.",
        }
    except Exception as exc:
        return {
            "safe": False,
            "flagged": True,
            "categories": {},
            "message": f"Moderation check error: {str(exc)}",
        }


def batch_check_annotations(
    annotations: List[MetricAnnotation],
    openai_api_key: Optional[str] = None,
    moderation_model: str = "text-moderation-latest",
) -> List[Dict[str, Any]]:
    """
    Check multiple metric annotations for unsafe text.

    Uses OpenAI text-moderation-latest model via the openai SDK.

    Args:
        annotations: List of MetricAnnotation objects to check.
        openai_api_key: OpenAI API key.
        moderation_model: OpenAI moderation model.

    Returns:
        List of safety check results, one per annotation.
    """
    results = []
    for annotation in annotations:
        result = check_annotation_safety(
            annotation=annotation,
            openai_api_key=openai_api_key,
            moderation_model=moderation_model,
        )
        result["annotation_title"] = annotation.title
        result["annotation_tags"] = annotation.tags
        results.append(result)
    return results


def validate_metric_label(
    label_text: str,
    openai_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validate a single metric label for safety.

    Quick wrapper around the OpenAI moderation API (text-moderation-latest).

    Args:
        label_text: The metric label text to validate.
        openai_api_key: OpenAI API key.

    Returns:
        Safety check result dict.
    """
    annotation = MetricAnnotation(
        title="Metric Label Validation",
        content=label_text,
    )
    return check_annotation_safety(annotation, openai_api_key=openai_api_key)
