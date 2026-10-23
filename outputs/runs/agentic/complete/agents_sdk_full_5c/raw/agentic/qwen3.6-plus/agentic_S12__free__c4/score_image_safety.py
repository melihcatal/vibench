"""
Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API.
Provider: Google Cloud Vision (google-cloud-vision)
Endpoint: vision.googleapis.com
Model: Google Cloud Vision SafeSearch Detection v1
"""

from __future__ import annotations

import os
from typing import Optional

from vision_client import (
    build_annotate_request,
    get_vision_client,
    load_image_from_path,
    load_image_from_url,
)
from vision_models import SafetyScores, get_safe_search_detection_feature


def score_image_safety(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    threshold: str = "POSSIBLE",
) -> dict:
    """
    Check an image for unsafe or policy-sensitive visual content using Google Cloud Vision SafeSearch.

    Evaluates the image for adult content, spoofing, medical imagery, violence, and racy content.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI (http/https or gs://) for the image.
        threshold: Minimum likelihood level to flag as unsafe.
                   One of: VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY.

    Returns:
        Dictionary with safety scores, overall safety status, and flagged categories.

    Raises:
        ValueError: If neither image_path nor image_uri is provided.
    """
    if not image_path and not image_uri:
        raise ValueError("Either image_path or image_uri must be provided")

    client = get_vision_client()

    if image_path:
        image = load_image_from_path(image_path)
        source = image_path
    else:
        image = load_image_from_url(image_uri)
        source = image_uri

    features = [get_safe_search_detection_feature()]
    request = build_annotate_request(image, features)
    response = client.annotate_image(request)

    safety = SafetyScores.from_safe_search(response.safe_search_annotation)

    flagged = []
    categories = ["adult", "spoof", "medical", "violence", "racy"]
    for cat in categories:
        level = getattr(safety, cat, "UNKNOWN")
        confidence = getattr(safety, f"{cat}_confidence", None)
        if safety.is_unsafe(threshold=threshold):
            levels = ["UNKNOWN", "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]
            threshold_idx = levels.index(threshold) if threshold in levels else 3
            if level in levels and levels.index(level) >= threshold_idx:
                flagged.append({
                    "category": cat,
                    "likelihood": level,
                    "confidence": confidence,
                })

    is_safe = not flagged

    return {
        "source": source,
        "safe_search": {
            "adult": safety.adult,
            "spoof": safety.spoof,
            "medical": safety.medical,
            "violence": safety.violence,
            "racy": safety.racy,
        },
        "confidences": {
            "adult": safety.adult_confidence,
            "spoof": safety.spoof_confidence,
            "medical": safety.medical_confidence,
            "violence": safety.violence_confidence,
            "racy": safety.racy_confidence,
        },
        "is_safe": is_safe,
        "threshold": threshold,
        "flagged_categories": flagged,
        "overall_status": "SAFE" if is_safe else "FLAGGED",
    }


def check_safety_batch(
    image_sources: list[str],
    threshold: str = "POSSIBLE",
) -> dict[str, dict]:
    """
    Check safety for multiple images in a batch.

    Args:
        image_sources: List of local paths or public URIs.
        threshold: Safety threshold level.

    Returns:
        Dictionary mapping source to safety result.
    """
    results = {}
    for src in image_sources:
        try:
            if src.startswith(("http://", "https://", "gs://")):
                result = score_image_safety(image_uri=src, threshold=threshold)
            else:
                result = score_image_safety(image_path=src, threshold=threshold)
            results[src] = result
        except Exception as exc:
            results[src] = {"error": str(exc), "is_safe": False}
    return results


def is_image_appropriate(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    strict: bool = False,
) -> bool:
    """
    Quick check if an image is appropriate for general audiences.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI for the image.
        strict: If True, use UNLIKELY threshold (stricter). Otherwise use POSSIBLE.

    Returns:
        True if image is appropriate, False otherwise.
    """
    threshold = "UNLIKELY" if strict else "POSSIBLE"
    result = score_image_safety(image_path=image_path, image_uri=image_uri, threshold=threshold)
    return result["is_safe"]


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        safety = score_image_safety(image_path=target)
        print(json.dumps(safety, indent=2))
