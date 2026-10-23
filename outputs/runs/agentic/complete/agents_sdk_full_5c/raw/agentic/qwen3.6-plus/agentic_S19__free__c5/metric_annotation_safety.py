"""
Check free-text metric labels or annotations for unsafe text.
Uses the OpenAI Moderation API as the concrete provider.
Provider: OpenAI (api.openai.com)
"""

from typing import Optional, Dict, Any, List

import openai


def metric_annotation_safety(
    annotations: List[str],
    model: str = "omni-moderation-latest",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Check free-text metric labels or annotations for unsafe text using
    the OpenAI Moderation API.

    Each annotation text is submitted to the OpenAI moderation endpoint
    to detect potentially harmful, illegal, or policy-violating content
    that may have been added as metric annotations or dashboard notes.

    Args:
        annotations: List of annotation/label text strings to check.
        model: OpenAI moderation model identifier (e.g. 'omni-moderation-latest').
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        base_url: Optional base URL override for OpenAI API.

    Returns:
        List of dicts with safety assessment for each annotation.
    """
    client_kwargs: Dict[str, Any] = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if base_url:
        client_kwargs["base_url"] = base_url

    client = openai.OpenAI(**client_kwargs)

    results: List[Dict[str, Any]] = []

    for annotation in annotations:
        if not annotation or not annotation.strip():
            results.append({
                "annotation": annotation,
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "safe": True,
            })
            continue

        try:
            moderation_response = client.moderations.create(
                input=annotation,
                model=model,
            )

            result_item = moderation_response.results[0]
            categories = {}
            category_scores = {}

            if hasattr(result_item, "categories"):
                for cat_name in dir(result_item.categories):
                    if not cat_name.startswith("_"):
                        val = getattr(result_item.categories, cat_name, None)
                        if val is not None:
                            categories[cat_name] = val

            if hasattr(result_item, "category_scores"):
                for score_name in dir(result_item.category_scores):
                    if not score_name.startswith("_"):
                        val = getattr(result_item.category_scores, score_name, None)
                        if val is not None:
                            category_scores[score_name] = val

            flagged = getattr(result_item, "flagged", False)

            results.append({
                "annotation": annotation,
                "flagged": flagged,
                "categories": categories,
                "category_scores": category_scores,
                "safe": not flagged,
            })
        except openai.APIError as e:
            results.append({
                "annotation": annotation,
                "flagged": True,
                "categories": {},
                "category_scores": {},
                "safe": False,
                "error": str(e),
            })

    return results


def check_annotation_safe(
    annotation: str,
    model: str = "omni-moderation-latest",
) -> bool:
    """
    Check if a single annotation text is safe.

    Args:
        annotation: The annotation text to check.
        model: OpenAI moderation model identifier.

    Returns:
        True if the annotation is safe (not flagged).
    """
    results = metric_annotation_safety([annotation], model=model)
    if results:
        return results[0].get("safe", True)
    return True


def get_unsafe_annotations(
    annotations: List[str],
    model: str = "omni-moderation-latest",
) -> List[str]:
    """
    Return only the annotations that were flagged as unsafe.

    Args:
        annotations: List of annotation texts to check.
        model: OpenAI moderation model identifier.

    Returns:
        List of annotation texts that were flagged.
    """
    results = metric_annotation_safety(annotations, model=model)
    return [r["annotation"] for r in results if r.get("flagged", False)]
