"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive visual content
using Google Cloud Vision API (google-cloud-vision SDK) Safe Search Detection.

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import sys
from typing import List, Optional

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums as vision_enums

from vision_client import (
    VisionClientManager,
    build_image_source,
    build_image_source_from_url,
    fetch_image_as_bytes,
)
from vision_models import (
    SafetyRating,
    SafetyScoreResponse,
)

# Google Cloud Vision safe search likelihood mappings to numeric scores
_LIKELIHOOD_SCORES = {
    "UNKNOWN": 0.0,
    "VERY_UNLIKELY": 0.0,
    "UNLIKELY": 0.15,
    "POSSIBLE": 0.5,
    "LIKELY": 0.8,
    "VERY_LIKELY": 1.0,
}

# Policy-sensitive threshold: ratings at or above this score are flagged
_POLICY_THRESHOLD = 0.5


def score_image_safety(
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    threshold: float = _POLICY_THRESHOLD,
) -> SafetyScoreResponse:
    """Check an image for unsafe or policy-sensitive content using Google Cloud Vision.

    Evaluates adult, violence, racy, spoof, and medical categories.

    Args:
        image_url: Public URL of the image to analyze.
        image_bytes: Raw image bytes (used if image_url is not provided).
        threshold: Numeric score threshold above which a category is flagged.

    Returns:
        SafetyScoreResponse with per-category ratings and overall safety verdict.
    """
    if not image_url and not image_bytes:
        raise ValueError("Either image_url or image_bytes must be provided.")

    client_manager = VisionClientManager()
    vision_client = client_manager.get_client()

    if image_url:
        image = build_image_source_from_url(image_url)
    else:
        image = build_image_source(image_bytes)

    feature = vision_v1.Feature(
        type_=vision_enums.Feature.Type.SAFE_SEARCH_DETECTION,
    )

    request = vision_v1.AnnotateImageRequest()
    request.image = image
    request.features = [feature]

    response = vision_client.annotate_image(request=request)
    safe_search = response.safe_search_annotation

    if not safe_search:
        return SafetyScoreResponse(
            ratings=[],
            is_safe=True,
            flagged_categories=[],
            raw_response={"status": "ok", "provider": "google-cloud-vision"},
        )

    categories = [
        ("adult", safe_search.adult),
        ("spoof", safe_search.spoof),
        ("medical", safe_search.medical),
        ("violence", safe_search.violence),
        ("racy", safe_search.racy),
    ]

    ratings: List[SafetyRating] = []
    flagged: List[str] = []

    for category_name, likelihood in categories:
        likelihood_str = str(likelihood).split(".")[-1].upper()
        score = _LIKELIHOOD_SCORES.get(likelihood_str, 0.0)
        rating = SafetyRating(
            category=category_name,
            likelihood=likelihood_str,
            likelihood_score=score,
        )
        ratings.append(rating)
        if score >= threshold:
            flagged.append(category_name)

    is_safe = len(flagged) == 0

    return SafetyScoreResponse(
        ratings=ratings,
        is_safe=is_safe,
        flagged_categories=flagged,
        raw_response={"status": "ok", "provider": "google-cloud-vision"},
    )


def score_image_safety_from_file(
    filepath: str,
    threshold: float = _POLICY_THRESHOLD,
) -> SafetyScoreResponse:
    """Check safety of a local image file using Google Cloud Vision."""
    with open(filepath, "rb") as fh:
        image_bytes = fh.read()
    return score_image_safety(image_bytes=image_bytes, threshold=threshold)


def format_safety_report(response: SafetyScoreResponse) -> str:
    """Format a human-readable safety score report."""
    lines = ["=== Image Safety Score Report (Google Cloud Vision) ===", ""]
    lines.append(f"Overall Safe: {response.is_safe}")
    if response.flagged_categories:
        lines.append(f"Flagged Categories: {', '.join(response.flagged_categories)}")
    else:
        lines.append("Flagged Categories: none")
    lines.append("")
    lines.append("Category Ratings:")
    for rating in response.ratings:
        score = rating.likelihood_score if rating.likelihood_score is not None else 0.0
        lines.append(
            f"  - {rating.category}: {rating.likelihood} (score: {score:.2f})"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_url_or_file>")
        sys.exit(1)

    source = sys.argv[1]
    if source.startswith(("http://", "https://")):
        result = score_image_safety(image_url=source)
    else:
        result = score_image_safety_from_file(source)

    print(format_safety_report(result))
