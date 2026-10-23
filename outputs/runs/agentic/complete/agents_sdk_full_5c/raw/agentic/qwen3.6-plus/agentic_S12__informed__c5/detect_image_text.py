"""
Detect text appearing inside a static image using Amazon Rekognition.

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
    TextDetectionRequest,
    TextDetectionResponse,
    DetectedText,
    normalize_rekognition_text,
)


def detect_image_text(
    image_source: Union[str, bytes, Path],
    language_hints: Optional[List[str]] = None,
    detect_orientation: bool = True,
    region: Optional[str] = None,
    custom_params: Optional[Dict[str, Any]] = None,
) -> TextDetectionResponse:
    """
    Detect text appearing inside a static image using Amazon Rekognition.

    Uses the Rekognition DetectText API to extract lines and words of text,
    along with their bounding boxes and confidence scores.

    Args:
        image_source: Path to image file, image bytes, or file-like object.
        language_hints: List of language codes (passed via custom_params).
        detect_orientation: Whether to apply orientation correction.
        region: AWS region override.
        custom_params: Additional parameters for the Rekognition API.

    Returns:
        TextDetectionResponse with detected text lines normalized to a unified format.
    """
    client = create_rekognition_client(region)

    image_payload = build_rekognition_image_payload(image_source)

    rekognition_params: Dict[str, Any] = {
        "Image": image_payload,
    }

    if detect_orientation:
        rekognition_params["Filters"] = {
            "WordFilter": {"MinConfidence": 0.0},
            "RegionsOfInterest": {"RegionFilter": {"MinConfidence": 0.0}},
        }

    # Merge custom parameters
    if custom_params:
        rekognition_params.update(custom_params)

    raw_response = client.detect_text(**rekognition_params)

    detected_texts = normalize_rekognition_text(raw_response)

    orientation_correction = raw_response.get("OrientationCorrection", 0)

    return TextDetectionResponse(
        detected_texts=detected_texts,
        orientation_correction=orientation_correction,
        text_model_version=raw_response.get("TextModelVersion", ""),
        request_id=raw_response.get("ResponseMetadata", {}).get("RequestId", ""),
        raw_response=raw_response,
    )


def detect_image_text_from_request(
    request: TextDetectionRequest,
    region: Optional[str] = None,
) -> TextDetectionResponse:
    """
    Detect text from a unified TextDetectionRequest object.

    Args:
        request: A TextDetectionRequest with image source and parameters.
        region: AWS region override.

    Returns:
        TextDetectionResponse with detected text.
    """
    return detect_image_text(
        image_source=request.image_source,
        language_hints=request.language_hints,
        detect_orientation=request.detect_orientation,
        region=region,
        custom_params=request.custom_params,
    )


def format_text_summary(response: TextDetectionResponse) -> str:
    """Format detected text into a human-readable summary string."""
    if not response.detected_texts:
        return "No text detected in the image."

    lines = ["Detected text regions:"]
    for i, text_item in enumerate(response.detected_texts, 1):
        box_info = ""
        if text_item.bounding_box:
            bb = text_item.bounding_box
            box_info = f" (position: left={bb.get('left', 0):.2f}, top={bb.get('top', 0):.2f})"
        lines.append(
            f"  {i}. \"{text_item.text}\" — {text_item.confidence:.1f}% confidence{box_info}"
        )

    if response.orientation_correction:
        lines.append(
            f"\nOrientation correction applied: {response.orientation_correction} degrees"
        )

    return "\n".join(lines)
