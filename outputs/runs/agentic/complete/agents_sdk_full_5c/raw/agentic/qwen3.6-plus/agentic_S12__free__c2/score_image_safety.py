"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive visual content.

Provider: Google Cloud Vision API (vision.googleapis.com)
Provider SDK: google-cloud-vision
Provider Identifying Signals: google.cloud.vision_v1.ImageAnnotatorClient,
                              GCLOUD_VISION_ env vars, vision.googleapis.com
"""

import os
import sys
import json
from typing import Optional, Dict, List

from vision_client import GoogleVisionClient, create_vision_client
from vision_models import (
    VisionImageRequest,
    ImageSafetyResponse,
    SafetyRating,
)


# Policy threshold mapping for different content moderation levels
SAFETY_THRESHOLDS = {
    "strict": 0.3,
    "moderate": 0.5,
    "lenient": 0.7,
}

# Google Cloud Vision SafeSearch categories
SAFE_SEARCH_CATEGORIES = [
    "adult",
    "spoof",
    "medical",
    "violence",
    "racy",
]


def score_image_safety(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    policy_level: str = "moderate",
    custom_thresholds: Optional[Dict[str, float]] = None,
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> ImageSafetyResponse:
    """
    Check a static image for unsafe or policy-sensitive visual content using
    Google Cloud Vision SafeSearch Detection.

    Args:
        image_path: Local path to the image file.
        image_uri: GCS URI of the image (gs://bucket/object).
        image_bytes: Raw image bytes.
        policy_level: Predefined policy level - "strict", "moderate", or "lenient".
        custom_thresholds: Optional per-category threshold overrides.
        credentials_path: Path to Google service account JSON credentials.
        project_id: Google Cloud project ID.

    Returns:
        ImageSafetyResponse with safety ratings and violation flags.

    Provider: Google Cloud Vision API
    Endpoint: vision.googleapis.com
    Feature: SAFE_SEARCH_DETECTION
    Categories: adult, spoof, medical, violence, racy
    """
    request = VisionImageRequest(
        image_path=image_path,
        image_uri=image_uri,
        image_bytes=image_bytes,
    )

    client = create_vision_client(
        credentials_path=credentials_path,
        project_id=project_id,
    )

    response = client.score_image_safety(request)

    if custom_thresholds:
        response.flagged_categories = [
            r.category for r in response.ratings
            if r.likelihood_score >= custom_thresholds.get(r.category, 0.5)
        ]
        response.is_safe = len(response.flagged_categories) == 0
    else:
        threshold = SAFETY_THRESHOLDS.get(policy_level, 0.5)
        response.flagged_categories = [
            r.category for r in response.ratings
            if r.likelihood_score >= threshold
        ]
        response.is_safe = len(response.flagged_categories) == 0

    return response


def check_image_safe(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    policy_level: str = "moderate",
    **kwargs,
) -> bool:
    """
    Convenience function that returns True if the image passes safety checks.
    """
    response = score_image_safety(
        image_path=image_path,
        image_uri=image_uri,
        image_bytes=image_bytes,
        policy_level=policy_level,
        **kwargs,
    )
    return response.is_safe


def format_safety_output(response: ImageSafetyResponse) -> str:
    """Format safety analysis results for display."""
    if response.error:
        return f"Error: {response.error}"

    lines = [
        "Safety Analysis:",
        f"  Overall safe: {'Yes' if response.is_safe else 'No'}",
        "",
        "Category Ratings:",
    ]

    for rating in response.ratings:
        status = "⚠ FLAGGED" if rating.category in response.flagged_categories else "✓ OK"
        lines.append(
            f"  {rating.category.capitalize():12s} "
            f"{rating.likelihood:16s} "
            f"(score: {rating.likelihood_score:.2f}) {status}"
        )

    if response.flagged_categories:
        lines.append("")
        lines.append(
            f"Flagged categories: {', '.join(response.flagged_categories)}"
        )

    return "\n".join(lines)


def safety_to_json(response: ImageSafetyResponse) -> str:
    """Serialize safety analysis results to JSON."""
    output = {
        "provider": "google_cloud_vision",
        "endpoint": "vision.googleapis.com",
        "feature": "SAFE_SEARCH_DETECTION",
        "error": response.error,
        "is_safe": response.is_safe,
        "flagged_categories": response.flagged_categories,
        "ratings": [
            {
                "category": r.category,
                "likelihood": r.likelihood,
                "likelihood_score": r.likelihood_score,
            }
            for r in response.ratings
        ],
    }
    return json.dumps(output, indent=2)


def main():
    """CLI entry point for safety scoring."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check an image for unsafe content using Google Cloud Vision SafeSearch"
    )
    parser.add_argument("image", help="Path to the image file or GCS URI")
    parser.add_argument(
        "--policy", default="moderate", choices=["strict", "moderate", "lenient"],
        help="Policy level for safety evaluation"
    )
    parser.add_argument(
        "--credentials", default=None,
        help="Path to Google service account JSON credentials"
    )
    parser.add_argument(
        "--project", default=None,
        help="Google Cloud project ID"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    is_gcs = args.image.startswith("gs://")

    if is_gcs:
        response = score_image_safety(
            image_uri=args.image,
            policy_level=args.policy,
            credentials_path=args.credentials,
            project_id=args.project,
        )
    else:
        response = score_image_safety(
            image_path=args.image,
            policy_level=args.policy,
            credentials_path=args.credentials,
            project_id=args.project,
        )

    if args.json:
        print(safety_to_json(response))
    else:
        print(format_safety_output(response))


if __name__ == "__main__":
    main()
