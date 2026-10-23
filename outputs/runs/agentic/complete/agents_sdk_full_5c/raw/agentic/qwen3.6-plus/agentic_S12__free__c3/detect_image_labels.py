"""
Detect labels or objects in a static image using AWS Rekognition.
Provider: AWS Rekognition (rekognition.us-east-1.amazonaws.com)
"""

from typing import List, Optional, Dict, Any

from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageLabel, ImageAnalysisPayload


def detect_labels_in_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    min_confidence: float = 70.0,
    max_labels: int = 50,
) -> ImageAnalysisPayload:
    """
    Detect labels and objects in a static image using AWS Rekognition.

    Uses the DetectLabels API to identify objects, scenes, and concepts
    present in the provided image.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        min_confidence: Minimum confidence threshold (0-100).
        max_labels: Maximum number of labels to return.

    Returns:
        ImageAnalysisPayload containing detected labels.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    client = get_rekognition_client()

    response = client.detect_labels(
        Image={"Bytes": raw_image},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = []
    for label_data in response.get("Labels", []):
        label = ImageLabel.from_rekognition(label_data)
        labels.append(label)

    payload = ImageAnalysisPayload(
        image_path=image_path,
        labels=labels,
        metadata={
            "provider": "aws_rekognition",
            "label_model": "rekognition-label-detection-v2",
            "labels_detected": len(labels),
            "label_model_version": response.get("LabelModelVersion", "unknown"),
        },
    )

    return payload


def detect_labels_batch(
    image_paths: List[str],
    min_confidence: float = 70.0,
    max_labels: int = 50,
) -> List[ImageAnalysisPayload]:
    """
    Detect labels in multiple images sequentially using AWS Rekognition.

    Args:
        image_paths: List of paths to image files.
        min_confidence: Minimum confidence threshold.
        max_labels: Maximum number of labels per image.

    Returns:
        List of ImageAnalysisPayload results.
    """
    results = []
    for img_path in image_paths:
        payload = detect_labels_in_image(
            image_path=img_path,
            min_confidence=min_confidence,
            max_labels=max_labels,
        )
        results.append(payload)
    return results


def get_top_labels(
    payload: ImageAnalysisPayload,
    top_n: int = 10,
) -> List[Dict[str, Any]]:
    """
    Extract the top N labels by confidence from analysis results.

    Args:
        payload: ImageAnalysisPayload from detect_labels_in_image.
        top_n: Number of top labels to return.

    Returns:
        List of label dictionaries sorted by confidence.
    """
    sorted_labels = sorted(payload.labels, key=lambda l: l.confidence, reverse=True)
    return [
        {"name": label.name, "confidence": label.confidence, "parents": label.parents}
        for label in sorted_labels[:top_n]
    ]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = detect_labels_in_image(image_path=sys.argv[1])
        top = get_top_labels(result, top_n=5)
        for label in top:
            print(f"{label['name']}: {label['confidence']:.1f}%")
