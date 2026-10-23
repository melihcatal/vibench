"""
Detects labels or objects in a static image using Google Cloud Vision API.
Provider: Google Cloud Vision (google-cloud-vision)
Endpoint: vision.googleapis.com
Model: Google Cloud Vision Label Detection v1
"""

from __future__ import annotations

import os
from typing import Optional

from google.cloud.vision_v1 import Feature

from vision_client import (
    build_annotate_request,
    get_vision_client,
    load_image_from_path,
    load_image_from_url,
)
from vision_models import LabelResult, get_label_detection_feature


def detect_labels(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    max_results: int = 20,
    include_object_localization: bool = False,
) -> list[LabelResult]:
    """
    Detect labels or objects in a static image using Google Cloud Vision API.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI (http/https or gs://) for the image.
        max_results: Maximum number of labels to return.
        include_object_localization: Whether to also run object localization.

    Returns:
        List of LabelResult objects with label name, confidence, and optional bounding box.

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

    features = [get_label_detection_feature(max_results=max_results)]

    if include_object_localization:
        features.append(Feature(type_=Feature.Type.OBJECT_LOCALIZATION))

    request = build_annotate_request(image, features)
    response = client.annotate_image(request)

    labels = []
    for entity in response.label_annotations:
        labels.append(LabelResult.from_entity(entity))

    if include_object_localization:
        for obj in response.localized_object_annotations:
            labels.append(
                LabelResult(
                    label=obj.name,
                    confidence=obj.score,
                    mid=obj.mid,
                )
            )

    return labels


def detect_labels_batch(
    image_paths: Optional[list[str]] = None,
    image_uris: Optional[list[str]] = None,
    max_results: int = 20,
) -> dict[str, list[LabelResult]]:
    """
    Detect labels across multiple images in a batch request.

    Args:
        image_paths: List of local image file paths.
        image_uris: List of public image URIs.
        max_results: Maximum labels per image.

    Returns:
        Dictionary mapping image source to list of LabelResult objects.
    """
    sources = []
    if image_paths:
        sources.extend(image_paths)
    if image_uris:
        sources.extend(image_uris)

    if not sources:
        raise ValueError("At least one image_path or image_uri must be provided")

    results = {}
    for src in sources:
        try:
            if src.startswith(("http://", "https://", "gs://")):
                labels = detect_labels(image_uri=src, max_results=max_results)
            else:
                labels = detect_labels(image_path=src, max_results=max_results)
            results[src] = labels
        except Exception as exc:
            results[src] = []
    return results


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        labels = detect_labels(image_path=target)
        output = [
            {"label": l.label, "confidence": l.confidence, "mid": l.mid}
            for l in labels
        ]
        print(json.dumps(output, indent=2))
