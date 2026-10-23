import os
import base64
from typing import Optional, List, Dict
import boto3
from botocore.config import Config

from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageSafetyRequest, ImageSafetyResponse, SafetyModerationLabel


UNSAFE_CATEGORIES = {
    "Explicit Nudity",
    "Suggestive",
    "Violence",
    "Visually Disturbing",
    "Hate Symbols",
    "Drugs",
    "Tobacco",
    "Alcohol",
    "Gambling",
    "Weapons",
}

SAFE_THRESHOLD = 75.0


def score_image_safety(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    custom_categories: Optional[List[str]] = None,
) -> ImageSafetyResponse:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    if image_bytes is None:
        image_bytes = load_image_bytes(image_path)

    client = get_rekognition_client()

    response = client.detect_moderation_labels(
        Image={"Bytes": image_bytes},
        MinConfidence=1.0,
    )

    categories_to_check = (
        set(custom_categories) if custom_categories else UNSAFE_CATEGORIES
    )

    moderation_labels = []
    unsafe_detections = []
    max_unsafe_confidence = 0.0

    for mod_label in response.get("ModerationLabels", []):
        label_name = mod_label.get("Name", "")
        parent_name = mod_label.get("ParentName", "")
        confidence = mod_label.get("Confidence", 0.0)

        safety_label = SafetyModerationLabel(
            name=label_name,
            parent_name=parent_name,
            confidence=confidence,
            category=mod_label.get("Name", ""),
        )
        moderation_labels.append(safety_label)

        category_match = (
            label_name in categories_to_check or parent_name in categories_to_check
        )
        if category_match and confidence >= SAFE_THRESHOLD:
            unsafe_detections.append(safety_label)
            max_unsafe_confidence = max(max_unsafe_confidence, confidence)

    is_safe = len(unsafe_detections) == 0
    safety_score = max(0.0, 100.0 - max_unsafe_confidence) if not is_safe else 100.0

    return ImageSafetyResponse(
        is_safe=is_safe,
        safety_score=safety_score,
        moderation_labels=moderation_labels,
        unsafe_detections=unsafe_detections,
        model="aws-rekognition-detect-moderation-labels-v3",
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_path>")
        sys.exit(1)

    result = score_image_safety(image_path=sys.argv[1])
    print(f"Safe: {result.is_safe}")
    print(f"Safety Score: {result.safety_score:.1f}")
    if result.unsafe_detections:
        print("Unsafe detections:")
        for det in result.unsafe_detections:
            print(f"  - {det.name}: {det.confidence:.1f}%")
