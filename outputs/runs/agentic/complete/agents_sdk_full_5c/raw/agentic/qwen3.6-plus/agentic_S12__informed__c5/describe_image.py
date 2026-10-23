"""
Generate a short visual description for a static image using Amazon Rekognition.

Provider: Amazon Rekognition (AWS)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from vision_client import (
    load_image_bytes,
    build_rekognition_image_payload,
    create_rekognition_client,
)
from vision_models import (
    ImageDescriptionRequest,
    ImageDescriptionResponse,
    ImageDescription,
    normalize_rekognition_labels,
)


def describe_image(
    image_source: Union[str, bytes, Path],
    max_descriptions: int = 5,
    language: str = "en",
    region: Optional[str] = None,
    custom_params: Optional[Dict[str, Any]] = None,
) -> ImageDescriptionResponse:
    """
    Generate a short visual description for an image using Amazon Rekognition.

    Uses Rekognition's label detection to extract the most prominent labels
    and constructs natural-language description candidates from them.
    Rekognition also provides tag-level metadata for scene understanding.

    Args:
        image_source: Path to image file, image bytes, or file-like object.
        max_descriptions: Maximum number of description candidates to generate.
        language: Language code for description output.
        region: AWS region override.
        custom_params: Additional parameters for Rekognition API.

    Returns:
        ImageDescriptionResponse with generated descriptions.
    """
    client = create_rekognition_client(region)

    image_payload = build_rekognition_image_payload(image_source)

    rekognition_params: Dict[str, Any] = {
        "Image": image_payload,
        "MaxLabels": max_descriptions * 3,  # request extra for richer descriptions
        "MinConfidence": 0.6,
    }

    if custom_params:
        rekognition_params.update(custom_params)

    raw_response = client.detect_labels(**rekognition_params)

    labels = normalize_rekognition_labels(raw_response)

    # Build descriptive tags from the top labels
    tags = [label.name for label in labels[:max_descriptions]]

    # Construct description from top-level labels
    if labels:
        top_labels = labels[:max_descriptions]
        label_names = [l.name.lower() for l in top_labels]

        # Use Rekognition scene understanding to build descriptions
        confidence_scores = [l.confidence for l in top_labels]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0

        description_text = _build_description_from_labels(label_names, language)
    else:
        description_text = "No significant visual elements detected."
        avg_confidence = 0.0

    descriptions = [
        ImageDescription(
            text=description_text,
            confidence=avg_confidence,
            tags=tags,
        )
    ]

    return ImageDescriptionResponse(
        descriptions=descriptions,
        tags=tags,
        request_id=raw_response.get("ResponseMetadata", {}).get("RequestId", ""),
        raw_response=raw_response,
    )


def _build_description_from_labels(labels: List[str], language: str) -> str:
    """
    Construct a natural-language description from Rekognition label names.

    Args:
        labels: List of label name strings from Rekognition.
        language: Language code (currently supports English).

    Returns:
        A descriptive sentence about the image content.
    """
    if not labels:
        return "An image with no clearly identifiable objects."

    if len(labels) == 1:
        return f"An image showing {labels[0]}."

    if len(labels) == 2:
        return f"An image showing {labels[0]} and {labels[1]}."

    # For 3+ labels, use the top two and summarize the rest
    main = f"{labels[0]} and {labels[1]}"
    remaining = labels[2:]
    return f"An image featuring {main} along with {', '.join(remaining)}."


def describe_image_from_request(
    request: ImageDescriptionRequest,
    region: Optional[str] = None,
) -> ImageDescriptionResponse:
    """
    Generate image descriptions from a unified ImageDescriptionRequest object.

    Args:
        request: An ImageDescriptionRequest with image source and parameters.
        region: AWS region override.

    Returns:
        ImageDescriptionResponse with generated descriptions.
    """
    return describe_image(
        image_source=request.image_source,
        max_descriptions=request.max_descriptions,
        language=request.language,
        region=region,
        custom_params=request.custom_params,
    )
