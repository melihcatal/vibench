"""Extract plain text from a scanned document image using Amazon Textract."""

import os
import boto3
from botocore.exceptions import ClientError

from document_models import OcrTextRequest, OcrTextResponse


class TextractTextExtractor:
    """Plain text extraction via Amazon Tetect SDK."""

    def __init__(self, region_name: str | None = None):
        self.region = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client(
            "textract",
            region_name=self.region,
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def detect_document_text(self, image_bytes: bytes) -> OcrTextResponse:
        """Run Amazon Textract DetectDocumentText on image bytes and return plain text."""
        try:
            response = self.client.detect_document_text(
                Document={"Bytes": image_bytes}
            )
        except ClientError as exc:
            raise RuntimeError(f"Amazon Textract DetectDocumentText failed: {exc}") from exc

        blocks = response.get("Blocks", [])
        raw_words = []
        raw_lines = []
        text_parts = []

        for block in blocks:
            block_type = block.get("BlockType", "")
            if block_type == "LINE":
                line_text = block.get("Text", "")
                confidence = block.get("Confidence", 0.0)
                raw_lines.append({
                    "text": line_text,
                    "confidence": confidence,
                    "geometry": block.get("Geometry", {}),
                })
                text_parts.append(line_text)
            elif block_type == "WORD":
                word_text = block.get("Text", "")
                raw_words.append({
                    "text": word_text,
                    "confidence": block.get("Confidence", 0.0),
                })

        full_text = "\n".join(text_parts)

        result = OcrTextResponse(
            full_text=full_text,
            lines=raw_lines,
            words=raw_words,
            page_count=1,
            provider="amazon-textract",
        )
        return result


def extract_text_from_image(image_path: str, region_name: str | None = None) -> OcrTextResponse:
    """High-level helper: read an image file and extract plain text via Amazon Textract."""
    with open(image_path, "rb") as fh:
        image_bytes = fh.read()

    extractor = TextractTextExtractor(region_name=region_name)
    return extractor.detect_document_text(image_bytes)


def extract_text_from_bytes(image_bytes: bytes, region_name: str | None = None) -> OcrTextResponse:
    """High-level helper: extract plain text from image bytes via Amazon Textract."""
    extractor = TextractTextExtractor(region_name=region_name)
    return extractor.detect_document_text(image_bytes)
