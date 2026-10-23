"""
describe_image.py - Generates a short visual description for an image
using Google Cloud Vision API (google-cloud-vision SDK) web detection.

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
from vision_models import ImageDescription


def describe_image(
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_labels: int = 10,
) -> ImageDescription:
    """Generate a visual description for an image using Google Cloud Vision.

    Uses LABEL_DETECTION and WEB_DETECTION features to build a rich description.

    Args:
        image_url: Public URL of the image to analyze.
        image_bytes: Raw image bytes (used if image_url is not provided).
        max_labels: Maximum number of label topics to include.

    Returns:
        ImageDescription with a generated description and confidence.
    """
    if not image_url and not image_bytes:
        raise ValueError("Either image_url or image_bytes must be provided.")

    client_manager = VisionClientManager()
    vision_client = client_manager.get_client()

    if image_url:
        image = build_image_source_from_url(image_url)
    else:
        image = build_image_source(image_bytes)

    features = [
        vision_v1.Feature(
            type_=vision_enums.Feature.Type.LABEL_DETECTION,
            max_results=max_labels,
        ),
        vision_v1.Feature(
            type_=vision_enums.Feature.Type.WEB_DETECTION,
        ),
        vision_v1.Feature(
            type_=vision_enums.Feature.Type.IMAGE_PROPERTIES,
        ),
    ]

    request = vision_v1.AnnotateImageRequest()
    request.image = image
    request.features = features

    response = vision_client.annotate_image(request=request)

    # Collect labels as topics
    topics: List[str] = []
    label_confidences: List[float] = []
    for label in response.label_annotations:
        topics.append(label.description)
        label_confidences.append(label.score)

    # Use web entity descriptions as supplementary topics
    if response.web_detection and response.web_detection.web_entities:
        for entity in response.web_detection.web_entities[:5]:
            if entity.description and entity.description not in topics:
                topics.append(entity.description)

    avg_confidence = 0.0
    if label_confidences:
        avg_confidence = sum(label_confidences) / len(label_confidences)

    # Build a descriptive sentence from top labels
    if topics:
        description = "The image shows " + ", ".join(topics[:5]) + "."
    else:
        description = "No visual description could be generated."

    return ImageDescription(
        description=description,
        confidence=avg_confidence,
        topics=topics[:max_labels],
        raw_response={"status": "ok", "provider": "google-cloud-vision"},
    )


def describe_image_from_file(
    filepath: str,
    max_labels: int = 10,
) -> ImageDescription:
    """Generate a visual description from a local image file."""
    with open(filepath, "rb") as fh:
        image_bytes = fh.read()
    return describe_image(image_bytes=image_bytes, max_labels=max_labels)


def format_description_report(desc: ImageDescription) -> str:
    """Format a human-readable description report."""
    lines = ["=== Image Description Report (Google Cloud Vision) ===", ""]
    lines.append(f"Description: {desc.description}")
    lines.append(f"Confidence:  {desc.confidence:.4f}")
    if desc.topics:
        lines.append("")
        lines.append("Topics:")
        for t in desc.topics:
            lines.append(f"  - {t}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_url_or_file>")
        sys.exit(1)

    source = sys.argv[1]
    if source.startswith(("http://", "https://")):
        result = describe_image(image_url=source)
    else:
        result = describe_image_from_file(source)

    print(format_description_report(result))
