"""
Generates a short visual description for an image using Google Cloud Vision API.
Provider: Google Cloud Vision (google-cloud-vision)
Endpoint: vision.googleapis.com
Model: Google Cloud Vision Web Detection / Label Detection v1
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
from vision_models import (
    ImageDescription,
    LabelResult,
    get_label_detection_feature,
    get_web_detection_feature,
)


def describe_image(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    max_labels: int = 10,
    include_web_entities: bool = True,
) -> dict:
    """
    Generate a short visual description for an image using Google Cloud Vision API.

    Uses label detection and optional web detection to build a descriptive summary
    of the image content.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI (http/https or gs://) for the image.
        max_labels: Maximum number of labels to use for description.
        include_web_entities: Whether to include web entity detection for richer context.

    Returns:
        Dictionary with description text, confidence, source labels, and web entities.

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

    features = [get_label_detection_feature(max_results=max_labels)]
    if include_web_entities:
        features.append(get_web_detection_feature(max_results=max_labels))

    request = build_annotate_request(image, features)
    response = client.annotate_image(request)

    labels = [LabelResult.from_entity(e) for e in response.label_annotations]
    web_descriptions = [
        ImageDescription.from_entity(e) for e in response.web_detection.web_entities
    ]

    full_descriptions = []
    for desc in response.web_detection.full_matching_images:
        full_descriptions.append(desc.url)

    best_guess_labels = [
        label.label for label in response.web_detection.best_guess_labels
    ]

    description_parts = []
    if best_guess_labels:
        description_parts.extend(best_guess_labels[:3])
    for label in labels[:5]:
        if label.label not in description_parts:
            description_parts.append(label.label)

    primary_description = ", ".join(description_parts[:5]) if description_parts else "No description available"

    web_entity_descriptions = []
    for entity in web_descriptions[:5]:
        web_entity_descriptions.append({
            "description": entity.description,
            "confidence": entity.confidence,
        })

    return {
        "source": source,
        "primary_description": primary_description,
        "description_parts": description_parts,
        "labels": [
            {"label": l.label, "confidence": l.confidence, "mid": l.mid}
            for l in labels
        ],
        "web_entities": web_entity_descriptions,
        "best_guess_labels": best_guess_labels,
        "full_matching_images_count": len(full_descriptions),
    }


def generate_alt_text(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    max_length: int = 125,
) -> str:
    """
    Generate accessibility-focused alt text for an image.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI for the image.
        max_length: Maximum character length for the alt text.

    Returns:
        A concise alt text string suitable for accessibility.
    """
    result = describe_image(image_path=image_path, image_uri=image_uri, max_labels=15)

    parts = result["description_parts"]
    if not parts:
        return "Image"

    alt_text = "Image showing " + ", ".join(parts[:4])

    if len(alt_text) > max_length:
        alt_text = alt_text[: max_length - 3] + "..."

    return alt_text


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        desc = describe_image(image_path=target)
        print(json.dumps(desc, indent=2))
