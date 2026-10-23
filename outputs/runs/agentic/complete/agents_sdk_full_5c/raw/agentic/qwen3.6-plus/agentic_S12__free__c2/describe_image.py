"""
describe_image.py - Generates a short visual description for an image.

Provider: Google Cloud Vision API (vision.googleapis.com)
Provider SDK: google-cloud-vision
Provider Identifying Signals: google.cloud.vision_v1.ImageAnnotatorClient,
                              GCLOUD_VISION_ env vars, vision.googleapis.com
"""

import os
import sys
import json
from typing import Optional

from vision_client import GoogleVisionClient, create_vision_client
from vision_models import (
    VisionImageRequest,
    ImageDescriptionResponse,
)


def describe_image(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_results: int = 10,
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> ImageDescriptionResponse:
    """
    Generate a short visual description for a static image using Google Cloud Vision API.

    Combines label detection, web detection, and image properties to produce
    a descriptive summary of the image content.

    Args:
        image_path: Local path to the image file.
        image_uri: GCS URI of the image (gs://bucket/object).
        image_bytes: Raw image bytes.
        max_results: Maximum number of results per feature.
        credentials_path: Path to Google service account JSON credentials.
        project_id: Google Cloud project ID.

    Returns:
        ImageDescriptionResponse with generated description and topics.

    Provider: Google Cloud Vision API
    Endpoint: vision.googleapis.com
    Features: LABEL_DETECTION, WEB_DETECTION, IMAGE_PROPERTIES
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

    response = client.describe_image(request, max_results=max_results)

    return response


def generate_alt_text(description: str, topics: list, max_length: int = 125) -> str:
    """
    Generate a concise alt-text suitable for accessibility from description and topics.
    """
    alt_text = description.strip()
    if len(alt_text) > max_length:
        alt_text = alt_text[: max_length - 3] + "..."
    return alt_text


def format_description_output(response: ImageDescriptionResponse) -> str:
    """Format description results for display."""
    if response.error:
        return f"Error: {response.error}"

    lines = [
        "Image Description:",
        f"  {response.description}",
        "",
        f"Confidence: {response.confidence:.3f}",
    ]

    if response.topics:
        lines.append(f"Topics: {', '.join(response.topics)}")

    alt = generate_alt_text(response.description, response.topics)
    lines.append(f"Alt Text: {alt}")

    return "\n".join(lines)


def description_to_json(response: ImageDescriptionResponse) -> str:
    """Serialize description results to JSON."""
    output = {
        "provider": "google_cloud_vision",
        "endpoint": "vision.googleapis.com",
        "features": ["LABEL_DETECTION", "WEB_DETECTION", "IMAGE_PROPERTIES"],
        "error": response.error,
        "description": response.description,
        "confidence": response.confidence,
        "topics": response.topics,
        "alt_text": generate_alt_text(response.description, response.topics),
    }
    return json.dumps(output, indent=2)


def main():
    """CLI entry point for image description."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a visual description for an image using Google Cloud Vision API"
    )
    parser.add_argument("image", help="Path to the image file or GCS URI")
    parser.add_argument(
        "--max-results", type=int, default=10,
        help="Maximum number of results per feature"
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
        response = describe_image(
            image_uri=args.image,
            max_results=args.max_results,
            credentials_path=args.credentials,
            project_id=args.project,
        )
    else:
        response = describe_image(
            image_path=args.image,
            max_results=args.max_results,
            credentials_path=args.credentials,
            project_id=args.project,
        )

    if args.json:
        print(description_to_json(response))
    else:
        print(format_description_output(response))


if __name__ == "__main__":
    main()
