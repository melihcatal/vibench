"""
Run OCR on a stored document object using Google Cloud Vision API.

Downloads the document from S3, then uses Google Cloud Vision
Document Text Detection to extract text with layout information.
"""

import os
from typing import Optional, List, Dict, Any
from io import BytesIO

import boto3
from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types
from google.api_core.exceptions import GoogleAPIError

from storage_client import get_s3_client, get_bucket_name
from storage_models import ObjectMetadataResponse
from object_metadata import get_object_metadata


GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_VISION_MAX_RESULTS = int(os.environ.get("GOOGLE_VISION_MAX_RESULTS", "100"))


class OcrBlock:
    """Represents a text block detected by Google Vision OCR."""

    def __init__(
        self,
        text: str,
        confidence: float,
        bounding_box: Optional[Dict[str, Any]] = None,
        block_type: str = "text",
    ):
        self.text = text
        self.confidence = confidence
        self.bounding_box = bounding_box
        self.block_type = block_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
            "block_type": self.block_type,
        }


class OcrResult:
    """Complete OCR result from Google Cloud Vision API."""

    def __init__(
        self,
        full_text: str,
        blocks: List[OcrBlock],
        page_count: int = 1,
        language_hints: Optional[List[str]] = None,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
    ):
        self.full_text = full_text
        self.blocks = blocks
        self.page_count = page_count
        self.language_hints = language_hints or []
        self.source_bucket = source_bucket
        self.source_key = source_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "full_text": self.full_text,
            "block_count": len(self.blocks),
            "blocks": [b.to_dict() for b in self.blocks],
            "page_count": self.page_count,
            "language_hints": self.language_hints,
            "source_bucket": self.source_bucket,
            "source_key": self.source_key,
        }


def _download_from_s3(bucket: str, key: str, s3_client=None) -> bytes:
    """Download object bytes from S3."""
    client = s3_client or get_s3_client()
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def _bounding_box_to_dict(vertices) -> Optional[Dict[str, Any]]:
    """Convert Google Vision bounding box vertices to a dictionary."""
    if not vertices:
        return None
    return {
        "vertices": [
            {"x": v.x, "y": v.y} for v in vertices
        ]
    }


def run_ocr_on_stored_document(
    key: str,
    bucket: Optional[str] = None,
    language_hints: Optional[List[str]] = None,
    s3_client=None,
) -> OcrResult:
    """
    Run Google Cloud Vision OCR on a document stored in S3.

    Args:
        key: S3 object key of the document
        bucket: S3 bucket name
        language_hints: List of language hints for OCR (e.g., ["en", "fr"])
        s3_client: Pre-configured boto3 S3 client

    Returns:
        OcrResult with extracted text and layout information
    """
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()

    # Verify object exists and is a supported type
    metadata = get_object_metadata(key=key, bucket=bucket_name, s3_client=client)
    if not metadata.exists:
        raise FileNotFoundError(f"Object not found: s3://{bucket_name}/{key}")

    # Download the document from S3
    image_bytes = _download_from_s3(bucket_name, key, s3_client=client)

    # Initialize Google Cloud Vision client
    # Provider signal: google.cloud.vision_v1.ImageAnnotatorClient
    vision_client = vision_v1.ImageAnnotatorClient()

    # Prepare the image for Vision API
    image = vision_types.Image(content=image_bytes)

    # Configure text detection with language hints
    image_context = vision_types.ImageContext()
    if language_hints:
        image_context.language_hints = language_hints

    # Perform document text detection (Google Cloud Vision API)
    response = vision_client.document_text_detection(
        image=image,
        image_context=image_context,
    )

    # Check for API errors
    if response.error.message:
        raise GoogleAPIError(f"Google Vision API error: {response.error.message}")

    # Parse the full document text
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""

    # Extract text blocks with confidence and bounding boxes
    blocks = []
    if response.full_text_annotation:
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_text = "".join(
                    word.text for paragraph in block.paragraphs for word in paragraph.words
                )
                confidence = block.confidence if block.confidence else 0.0
                bbox = _bounding_box_to_dict(block.bounding_box.vertices)

                # Determine block type from block type enum
                block_type_map = {
                    vision_types.Block.Type.TEXT: "text",
                    vision_types.Block.Type.TABLE: "table",
                    vision_types.Block.Type.PICTURE: "picture",
                    vision_types.Block.Type.RULER: "ruler",
                    vision_types.Block.Type.BARCODE: "barcode",
                }
                block_type = block_type_map.get(block.block_type, "unknown")

                blocks.append(OcrBlock(
                    text=block_text,
                    confidence=confidence,
                    bounding_box=bbox,
                    block_type=block_type,
                ))

    page_count = len(response.full_text_annotation.pages) if response.full_text_annotation else 1

    return OcrResult(
        full_text=full_text,
        blocks=blocks,
        page_count=page_count,
        language_hints=language_hints or [],
        source_bucket=bucket_name,
        source_key=key,
    )


def extract_text_from_stored_document(
    key: str,
    bucket: Optional[str] = None,
    s3_client=None,
) -> str:
    """
    Extract plain text from a stored document using Google Vision OCR.

    Args:
        key: S3 object key
        bucket: S3 bucket name
        s3_client: Pre-configured boto3 S3 client

    Returns:
        Extracted plain text string
    """
    result = run_ocr_on_stored_document(key, bucket=bucket, s3_client=s3_client)
    return result.full_text
