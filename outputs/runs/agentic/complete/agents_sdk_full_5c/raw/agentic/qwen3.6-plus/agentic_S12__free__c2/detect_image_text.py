"""
detect_image_text.py - Detects text appearing inside an image (OCR).

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
from vision_models import (
    VisionImageRequest,
    ImageTextResponse,
    DetectedText,
)


def detect_text(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    language_hints: Optional[List[str]] = None,
    document_mode: bool = False,
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> ImageTextResponse:
    """
    Detect text in a static image using Google Cloud Vision API OCR.

    Supports both general TEXT_DETECTION and dense DOCUMENT_TEXT_DETECTION modes.

    Args:
        image_path: Local path to the image file.
        image_uri: GCS URI of the image (gs://bucket/object).
        image_bytes: Raw image bytes.
        language_hints: List of BCP-47 language codes to improve accuracy.
        document_mode: If True, use DOCUMENT_TEXT_DETECTION for dense text.
        credentials_path: Path to Google service account JSON credentials.
        project_id: Google Cloud project ID.

    Returns:
        ImageTextResponse with detected text blocks and full text.

    Provider: Google Cloud Vision API
    Endpoint: vision.googleapis.com
    Features: TEXT_DETECTION or DOCUMENT_TEXT_DETECTION
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

    if document_mode:
        response = client.detect_document_text(
            request, language_hints=language_hints
        )
    else:
        response = client.detect_text(
            request, language_hints=language_hints
        )

    return response


def extract_text_blocks(
    response: ImageTextResponse,
    min_confidence: float = 0.0,
) -> List[Dict]:
    """Extract individual text blocks above a confidence threshold."""
    blocks = []
    for text in response.texts:
        if text.confidence >= min_confidence:
            blocks.append({
                "text": text.text,
                "confidence": text.confidence,
                "language": text.language,
                "bounding_poly": text.bounding_poly,
            })
    return blocks


def format_text_output(response: ImageTextResponse) -> str:
    """Format OCR results for display."""
    if response.error:
        return f"Error: {response.error}"

    if not response.full_text:
        return "No text detected in the image."

    lines = [
        "Detected Text:",
        f"  Full text: {response.full_text[:200]}",
        "",
        f"Text blocks found: {len(response.texts)}",
    ]

    if response.texts:
        lines.append("")
        lines.append("Individual text segments:")
        for i, text in enumerate(response.texts[:10], 1):
            lines.append(
                f"  {i}. \"{text.text}\" (confidence: {text.confidence:.3f})"
            )
        if len(response.texts) > 10:
            lines.append(f"  ... and {len(response.texts) - 10} more segments")

    return "\n".join(lines)


def text_to_json(response: ImageTextResponse) -> str:
    """Serialize OCR results to JSON."""
    output = {
        "provider": "google_cloud_vision",
        "endpoint": "vision.googleapis.com",
        "feature": "TEXT_DETECTION",
        "error": response.error,
        "full_text": response.full_text,
        "text_blocks": [
            {
                "text": t.text,
                "confidence": t.confidence,
                "language": t.language,
            }
            for t in response.texts
        ],
    }
    return json.dumps(output, indent=2)


def main():
    """CLI entry point for text detection."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect text in an image using Google Cloud Vision API OCR"
    )
    parser.add_argument("image", help="Path to the image file or GCS URI")
    parser.add_argument(
        "--languages", nargs="+", default=None,
        help="BCP-47 language hints (e.g., en, fr, es)"
    )
    parser.add_argument(
        "--document", action="store_true",
        help="Use DOCUMENT_TEXT_DETECTION for dense text"
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
        response = detect_text(
            image_uri=args.image,
            language_hints=args.languages,
            document_mode=args.document,
            credentials_path=args.credentials,
            project_id=args.project,
        )
    else:
        response = detect_text(
            image_path=args.image,
            language_hints=args.languages,
            document_mode=args.document,
            credentials_path=args.credentials,
            project_id=args.project,
        )

    if args.json:
        print(text_to_json(response))
    else:
        print(format_text_output(response))


if __name__ == "__main__":
    main()
