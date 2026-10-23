"""
Check generated visual labels for unsafe text using OpenAI Moderation API.
Provider: OpenAI Moderation (api.openai.com/v1/moderations) - text-moderation-latest model
"""

from typing import List, Optional, Dict, Any

from openai import OpenAI

from vision_client import get_openai_client
from vision_models import ImageAnalysisPayload


MODERATION_CATEGORIES = [
    "hate",
    "hate/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def check_visual_labels_safety(
    payload: ImageAnalysisPayload,
    model: str = "text-moderation-latest",
) -> dict:
    """
    Check generated visual labels and descriptions for unsafe content using OpenAI Moderation.

    Extracts text from detected labels, image descriptions, and OCR text,
    then runs them through the OpenAI Moderation API to flag policy violations.

    Args:
        payload: ImageAnalysisPayload containing visual analysis results.
        model: OpenAI moderation model (default: text-moderation-latest).

    Returns:
        Dictionary with moderation results and flagged categories.
    """
    texts_to_check = _extract_texts_from_payload(payload)
    combined_text = " ".join(texts_to_check)

    if not combined_text.strip():
        return {
            "flagged": False,
            "categories": {},
            "texts_checked": 0,
            "provider": "openai_moderation",
            "model": model,
            "endpoint": "https://api.openai.com/v1/moderations",
            "note": "No text content to moderate",
        }

    client = get_openai_client()

    response = client.moderations.create(
        model=model,
        input=combined_text,
    )

    result = response.results[0]

    flagged_categories = []
    category_scores = {}
    for cat in MODERATION_CATEGORIES:
        score = getattr(result.category_scores, cat.replace("/", "_").replace("-", "_"), 0)
        is_flagged = getattr(result.categories, cat.replace("/", "_").replace("-", "_"), False)
        category_scores[cat] = score
        if is_flagged:
            flagged_categories.append(cat)

    return {
        "flagged": result.flagged,
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "texts_checked": len(texts_to_check),
        "combined_text_length": len(combined_text),
        "provider": "openai_moderation",
        "model": model,
        "model_family": "text-moderation",
        "endpoint": "https://api.openai.com/v1/moderations",
    }


def check_text_safety(
    text: str,
    model: str = "text-moderation-latest",
) -> dict:
    """
    Check arbitrary text for unsafe content using OpenAI Moderation API.

    Args:
        text: Text to check.
        model: OpenAI moderation model.

    Returns:
        Dictionary with moderation results.
    """
    if not text.strip():
        return {"flagged": False, "note": "Empty text"}

    client = get_openai_client()

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": {
            cat: getattr(result.categories, cat.replace("/", "_").replace("-", "_"), False)
            for cat in MODERATION_CATEGORIES
        },
        "scores": {
            cat: getattr(result.category_scores, cat.replace("/", "_").replace("-", "_"), 0)
            for cat in MODERATION_CATEGORIES
        },
        "provider": "openai_moderation",
        "model": model,
    }


def _extract_texts_from_payload(payload: ImageAnalysisPayload) -> List[str]:
    """Extract all text content from an ImageAnalysisPayload for moderation."""
    texts = []

    # Labels
    for label in payload.labels:
        texts.append(label.name)
        texts.extend(label.parents)

    # Description
    if payload.description:
        texts.append(payload.description.text)

    # Detected text
    for detected in payload.detected_texts:
        texts.append(detected.text)

    return [t for t in texts if t and t.strip()]


def get_safety_verdict(
    payload: ImageAnalysisPayload,
    threshold: float = 0.5,
    model: str = "text-moderation-latest",
) -> Dict[str, Any]:
    """
    Get a simple pass/fail safety verdict for visual analysis content.

    Args:
        payload: ImageAnalysisPayload to check.
        threshold: Score threshold for flagging (0.0-1.0).
        model: Moderation model to use.

    Returns:
        Dictionary with verdict and supporting details.
    """
    moderation = check_visual_labels_safety(payload, model=model)

    high_score_categories = [
        cat for cat, score in moderation.get("category_scores", {}).items()
        if score >= threshold
    ]

    return {
        "safe": not moderation["flagged"] and len(high_score_categories) == 0,
        "flagged": moderation["flagged"],
        "high_score_categories": high_score_categories,
        "provider": "openai_moderation",
        "model": model,
    }


if __name__ == "__main__":
    from detect_image_labels import detect_labels_in_image
    import sys

    if len(sys.argv) > 1:
        payload = detect_labels_in_image(image_path=sys.argv[1])
        result = check_visual_labels_safety(payload)
        print(f"Flagged: {result['flagged']}")
        if result['flagged']:
            print(f"Categories: {result['flagged_categories']}")
