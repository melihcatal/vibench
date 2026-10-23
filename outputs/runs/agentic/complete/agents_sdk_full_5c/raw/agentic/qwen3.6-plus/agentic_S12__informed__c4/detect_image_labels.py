"""
detect_image_labels.py - Detects labels or objects in a static image
using Google Cloud Vision API (google-cloud-vision SDK).

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums as vision_enums

from vision_client import (
    VisionClientManager,
    build_image_source,
    build_image_source_from_url,
    build_label_detection_config,
    fetch_image_as_bytes,
)
from vision_models import (
    ImageAnalysisRequest,
    LabelDetectionResponse,
    LabelResult,
)


def detect_labels(
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_results: int = 10,
) -> LabelDetectionResponse:
    """Detect labels/objects in an image using Google Cloud Vision.

    Args:
        image_url: Public URL of the image to analyze.
        image_bytes: Raw image bytes (used if image_url is not provided).
        max_results: Maximum number of labels to return.

    Returns:
        LabelDetectionResponse containing detected labels with confidence scores.
    """
    if not image_url and not image_bytes:
        raise ValueError("Either image_url or image_bytes must be provided.")

    client_manager = VisionClientManager()
    vision_client = client_manager.get_client()

    if image_url:
        image = build_image_source_from_url(image_url)
    else:
        image = build_image_source(image_bytes)

    feature = build_label_detection_config(max_results=max_results)

    request = vision_v1.AnnotateImageRequest()
    request.image = image
    request.features = [feature]

    response = vision_client.annotate_image(request=request)

    labels: List[LabelResult] = []
    for label_annotation in response.label_annotations:
        mid_value = label_annotation.mid if label_annotation.mid else None
        labels.append(
            LabelResult(
                label=label_annotation.description,
                confidence=label_annotation.score,
                mid=mid_value,
            )
        )

    # Sort by confidence descending
    labels.sort(key=lambda l: l.confidence, reverse=True)

    return LabelDetectionResponse(
        labels=labels,
        raw_response={"status": "ok", "provider": "google-cloud-vision"},
    )


def detect_labels_from_file(
    filepath: str,
    max_results: int = 10,
) -> LabelDetectionResponse:
    """Detect labels from a local image file using Google Cloud Vision.

    Args:
        filepath: Path to the local image file.
        max_results: Maximum number of labels to return.

    Returns:
        LabelDetectionResponse with detected labels.
    """
    with open(filepath, "rb") as fh:
        image_bytes = fh.read()
    return detect_labels(image_bytes=image_bytes, max_results=max_results)


def format_labels_report(response: LabelDetectionResponse) -> str:
    """Format a human-readable labels report."""
    lines = ["=== Image Label Detection Report (Google Cloud Vision) ===", ""]
    if not response.labels:
        lines.append("No labels detected.")
        return "\n".join(lines)
    for i, label in enumerate(response.labels, 1):
        lines.append(
            f"  {i}. {label.label} (confidence: {label.confidence:.4f})"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_url_or_file>")
        sys.exit(1)

    source = sys.argv[1]
    if source.startswith(("http://", "https://")):
        result = detect_labels(image_url=source)
    else:
        result = detect_labels_from_file(source)

    print(format_labels_report(result))
