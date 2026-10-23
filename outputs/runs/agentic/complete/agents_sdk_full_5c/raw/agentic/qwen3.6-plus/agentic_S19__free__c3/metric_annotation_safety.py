"""
metric_annotation_safety.py
Check free-text metric labels or annotations for unsafe text using the OpenAI Moderation API.
Provider: OpenAI (api.openai.com)
"""

import os
from typing import List, Optional, Dict, Any, Tuple

import openai

from observability_models import MetricAnnotation


def check_annotation_safety(
    annotation_text: str,
    model: str = "omni-moderation-latest",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check a metric annotation or dashboard note for unsafe content
    using the OpenAI Moderation API.

    Args:
        annotation_text: The free-text metric annotation to check.
        model: The OpenAI moderation model to use (default omni-moderation-latest).
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).

    Returns:
        Dict with safety analysis results including flagged categories and overall verdict.
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)

    try:
        moderation_result = client.moderations.create(
            input=annotation_text,
            model=model,
        )

        result = moderation_result.results[0] if moderation_result.results else None

        if result is None:
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "verdict": "safe",
                "input_text": annotation_text,
            }

        categories = {}
        category_scores = {}

        # Extract category flags and scores
        for cat_name in [
            "sexual", "hate", "harassment", "self-harm",
            "sexual/minors", "hate/threatening", "violence/graphic",
            "self-harm/intent", "self-harm/instructions",
            "harassment/threatening", "violence",
        ]:
            flag_val = getattr(result.flagged_categories, cat_name, None)
            score_val = getattr(result.category_scores, cat_name, None)
            if flag_val is not None:
                categories[cat_name] = flag_val
            if score_val is not None:
                category_scores[cat_name] = score_val

        # Fallback: check dict-style access for newer SDK versions
        if not categories and hasattr(result, 'categories'):
            cats = result.categories
            if isinstance(cats, dict):
                categories = cats
            else:
                categories = {k: getattr(cats, k, False) for k in dir(cats) if not k.startswith('_')}

        if not category_scores and hasattr(result, 'category_scores'):
            scores = result.category_scores
            if isinstance(scores, dict):
                category_scores = scores
            else:
                category_scores = {k: getattr(scores, k, 0.0) for k in dir(scores) if not k.startswith('_') and k != 'to_dict'}

        flagged = result.flagged

        verdict = "unsafe" if flagged else "safe"

        return {
            "flagged": flagged,
            "categories": categories,
            "category_scores": {k: round(v, 4) for k, v in category_scores.items() if isinstance(v, (int, float))},
            "verdict": verdict,
            "input_text": annotation_text,
        }

    except openai.APIError as exc:
        raise RuntimeError(
            f"OpenAI moderation API call failed for annotation: {exc}"
        ) from exc


def batch_check_annotations(
    annotations: List[str],
    model: str = "omni-moderation-latest",
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Check multiple metric annotations for unsafe content via OpenAI Moderation.

    Args:
        annotations: List of annotation texts to check.
        model: OpenAI moderation model to use.
        api_key: Optional OpenAI API key.

    Returns:
        List of safety result dicts, one per annotation.
    """
    results = []
    for text in annotations:
        result = check_annotation_safety(
            annotation_text=text,
            model=model,
            api_key=api_key,
        )
        results.append(result)
    return results


def sanitize_metric_annotation(
    annotation_text: str,
    model: str = "omni-moderation-latest",
    api_key: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Check and optionally sanitize a metric annotation using OpenAI Moderation.

    Returns a tuple of (is_safe, cleaned_text). If flagged, the text is
    returned as-is with a note about the safety check failure.

    Args:
        annotation_text: The annotation to check.
        model: OpenAI moderation model.
        api_key: Optional OpenAI API key.

    Returns:
        Tuple of (is_safe, sanitized_text).
    """
    result = check_annotation_safety(annotation_text, model=model, api_key=api_key)

    if result["flagged"]:
        flagged_categories = [cat for cat, flagged in result["categories"].items() if flagged]
        sanitized = f"[REDACTED - flagged for: {', '.join(flagged_categories)}]"
        return False, sanitized

    return True, annotation_text


def validate_metric_label(
    label_text: str,
    model: str = "omni-moderation-latest",
    api_key: Optional[str] = None,
) -> bool:
    """
    Validate that a metric label is safe using OpenAI Moderation API.

    Args:
        label_text: The metric label text to validate.
        model: OpenAI moderation model.
        api_key: Optional OpenAI API key.

    Returns:
        True if the label is safe, False otherwise.
    """
    result = check_annotation_safety(label_text, model=model, api_key=api_key)
    return not result["flagged"]
