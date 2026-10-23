from __future__ import annotations

from google.cloud import vision

from vision_client import build_client, make_image
from vision_models import DescriptionResult


def describe_image(image_path: str) -> DescriptionResult:
    client = build_client()
    image = make_image(image_path)
    response = client.label_detection(image=image, max_results=5)
    labels = response.label_annotations
    if not labels:
        return DescriptionResult(description="An image with no clearly identified subject.", confidence=0.0)
    top = labels[0]
    description = f"A photo featuring {top.description.lower()} and related objects."
    return DescriptionResult(description=description, confidence=float(getattr(top, "score", 0.0) or 0.0))
