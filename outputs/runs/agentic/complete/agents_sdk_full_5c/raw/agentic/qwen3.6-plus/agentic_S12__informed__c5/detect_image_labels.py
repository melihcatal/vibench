"""
Detect labels or objects in a static image using Amazon Rekognition.

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
    LabelDetectionRequest,
    LabelDetectionResponse,
    DetectedLabel,
    normalize_rekognition_labels,
    filter_by_confidence,
)


def detect_image_labels(
    image_source: Union[str, bytes, Path],
    max_labels: int = 50,
    min_confidence: float = 0.5,
    region: Optional[str] = None,
    custom_params: Optional[Dict[str, Any]] = None,
) -> LabelDetectionResponse:
    """
    Detect labels and objects in a static image using Amazon Rekognition.

    Args:
        image_source: Path to image file, image bytes, or file-like object.
        max_labels: Maximum number of labels to return.
        min_confidence: Minimum confidence threshold for returned labels.
        region: AWS region override (defaults to AWS_DEFAULT_REGION env var).
        custom_params: Additional parameters to pass to Rekognition.

    Returns:
        LabelDetectionResponse with detected labels normalized to a unified format.
    """
    client = create_rekognition_client(region)

    image_payload = build_rekognition_image_payload(image_source)

    rekognition_params: Dict[str, Any] = {
        "Image": image_payload,
        "MaxLabels": max_labels,
        "MinConfidence": min_confidence,
    }

    # Merge any custom parameters
    if custom_params:
        rekognition_params.update(custom_params)

    raw_response = client.detect_labels(**rekognition_params)

    labels = normalize_rekognition_labels(raw_response)
    labels = filter_by_confidence(labels, min_confidence)

    return LabelDetectionResponse(
        labels=labels,
        label_model_version=raw_response.get("LabelModelVersion", ""),
        request_id=raw_response.get("ResponseMetadata", {}).get("RequestId", ""),
        raw_response=raw_response,
    )


def detect_image_labels_from_request(
    request: LabelDetectionRequest,
    region: Optional[str] = None,
) -> LabelDetectionResponse:
    """
    Detect labels from a unified LabelDetectionRequest object.

    Args:
        request: A LabelDetectionRequest with image source and parameters.
        region: AWS region override.

    Returns:
        LabelDetectionResponse with detected labels.
    """
    return detect_image_labels(
        image_source=request.image_source,
        max_labels=request.max_labels,
        min_confidence=request.min_confidence,
        region=region,
        custom_params=request.custom_params,
    )


def format_labels_summary(response: LabelDetectionResponse) -> str:
    """Format detected labels into a human-readable summary string."""
    if not response.labels:
        return "No labels detected."

    lines = ["Detected labels:"]
    for label in response.labels:
        instance_info = ""
        if label.instances:
            instance_info = f" ({len(label.instances)} instance(s))"
        parent_info = ""
        if label.parents:
            parent_info = f" [parents: {', '.join(label.parents)}]"
        lines.append(
            f"  - {label.name}: {label.confidence:.1f}% confidence"
            f"{instance_info}{parent_info}"
        )
    return "\n".join(lines)
