"""
detect_image_labels.py - Detects labels or objects in a static image
using Azure AI Vision Image Analysis SDK.
"""

import os
import sys
from typing import List, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import (
    create_image_analysis_client,
    read_image_bytes,
)
from vision_models import DetectedLabel, normalize_label_from_azure


def detect_image_labels(
    image_path: str,
    *,
    confidence_threshold: float = 0.5,
    client: Optional[ImageAnalysisClient] = None,
) -> List[DetectedLabel]:
    """
    Detect labels and objects in a static image using Azure AI Vision.

    Provider: Azure AI Vision (azure-ai-vision-imageanalysis)
    Auth: AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
    """
    if client is None:
        client = create_image_analysis_client()

    image_bytes = read_image_bytes(image_path)

    features = [
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
    ]

    result = client.analyze(
        image_data=image_bytes,
        visual_features=features,
    )

    labels: List[DetectedLabel] = []

    # Process detected objects
    if result.objects is not None:
        for obj in result.objects.objects:
            if obj.confidence is not None and obj.confidence >= confidence_threshold:
                label = DetectedLabel(
                    name=obj.tags[0].name if obj.tags else "",
                    confidence=float(obj.confidence),
                    bounding_box={
                        "x": obj.bounding_box.x,
                        "y": obj.bounding_box.y,
                        "w": obj.bounding_box.w,
                        "h": obj.bounding_box.h,
                    }
                    if obj.bounding_box
                    else None,
                )
                labels.append(label)

    # Process detected tags/labels
    if result.tags is not None:
        for tag in result.tags:
            if tag.confidence is not None and tag.confidence >= confidence_threshold:
                # Avoid duplicate names
                if not any(l.name.lower() == tag.name.lower() for l in labels):
                    label = DetectedLabel(
                        name=tag.name or "",
                        confidence=float(tag.confidence),
                    )
                    labels.append(label)

    labels.sort(key=lambda l: l.confidence, reverse=True)
    return labels


def format_labels_report(labels: List[DetectedLabel]) -> str:
    """Format detected labels into a human-readable report."""
    if not labels:
        return "No labels detected above the confidence threshold."

    lines = ["Detected Labels:"]
    for label in labels:
        bbox_info = ""
        if label.bounding_box:
            bbox_info = (
                f" [box: ({label.bounding_box['x']}, {label.bounding_box['y']}), "
                f"{label.bounding_box['w']}x{label.bounding_box['h']}]"
            )
        lines.append(
            f"  - {label.name} ({label.confidence:.2%}){bbox_info}"
        )
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path> [confidence_threshold]")
        sys.exit(1)

    image_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    labels = detect_image_labels(image_path, confidence_threshold=threshold)
    report = format_labels_report(labels)
    print(report)


if __name__ == "__main__":
    main()
