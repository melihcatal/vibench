"""
detect_image_labels.py - Detects labels or objects in a static image.

Provider: Google Cloud Vision API (vision.googleapis.com)
Provider SDK: google-cloud-vision
Provider Identifying Signals: google.cloud.vision_v1.ImageAnnotatorClient,
                              GCLOUD_VISION_ env vars, vision.googleapis.com
"""

import os
import sys
import json
from typing import List, Optional

from vision_client import GoogleVisionClient, create_vision_client
from vision_models import VisionImageRequest, ImageLabelsResponse, ImageLabel


def detect_labels(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_results: int = 10,
    score_threshold: float = 0.0,
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> ImageLabelsResponse:
    """
    Detect labels/objects in a static image using Google Cloud Vision API.

    Args:
        image_path: Local path to the image file.
        image_uri: GCS URI of the image (gs://bucket/object).
        image_bytes: Raw image bytes.
        max_results: Maximum number of labels to return (default 10).
        score_threshold: Minimum confidence score to include a label.
        credentials_path: Path to Google service account JSON credentials.
        project_id: Google Cloud project ID.

    Returns:
        ImageLabelsResponse with detected labels, scores, and metadata.

    Provider: Google Cloud Vision API
    Endpoint: vision.googleapis.com
    Feature: LABEL_DETECTION
    """
    request = VisionImageRequest(
        image_path=image_path,
        image_uri=image_uri,
        image_bytes=image_bytes,
    )

    client = create_vision_client(
        credentials_path=credentials_path,
        project_id=project_id,
    )

    response = client.detect_labels(request, max_results=max_results)

    if response.labels:
        response.labels = [
            label for label in response.labels
            if label.score >= score_threshold
        ]

    return response


def format_labels_output(response: ImageLabelsResponse) -> str:
    """Format label detection results for display."""
    if response.error:
        return f"Error: {response.error}"

    if not response.labels:
        return "No labels detected."

    lines = ["Detected Labels:"]
    for i, label in enumerate(response.labels, 1):
        lines.append(
            f"  {i}. {label.description} "
            f"(score: {label.score:.3f}, "
            f"confidence: {label.confidence:.3f})"
        )
    return "\n".join(lines)


def detect_labels_to_json(response: ImageLabelsResponse) -> str:
    """Serialize label detection results to JSON."""
    output = {
        "provider": "google_cloud_vision",
        "endpoint": "vision.googleapis.com",
        "feature": "LABEL_DETECTION",
        "error": response.error,
        "labels": [
            {
                "description": label.description,
                "score": label.score,
                "confidence": label.confidence,
                "topicality": label.topicality,
                "mid": label.mid,
            }
            for label in response.labels
        ],
    }
    return json.dumps(output, indent=2)


def main():
    """CLI entry point for label detection."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect labels in an image using Google Cloud Vision API"
    )
    parser.add_argument("image", help="Path to the image file or GCS URI")
    parser.add_argument(
        "--max-results", type=int, default=10,
        help="Maximum number of labels to return"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.0,
        help="Minimum confidence score threshold"
    )
    parser.add_argument(
        "--credentials", default=None,
        help="Path to Google service account JSON credentials"
    )
    parser.add_argument(
        "--project", default=None,
        help="Google Cloud project ID"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    is_gcs = args.image.startswith("gs://")

    if is_gcs:
        response = detect_labels(
            image_uri=args.image,
            max_results=args.max_results,
            score_threshold=args.threshold,
            credentials_path=args.credentials,
            project_id=args.project,
        )
    else:
        response = detect_labels(
            image_path=args.image,
            max_results=args.max_results,
            score_threshold=args.threshold,
            credentials_path=args.credentials,
            project_id=args.project,
        )

    if args.json:
        print(detect_labels_to_json(response))
    else:
        print(format_labels_output(response))


if __name__ == "__main__":
    main()
