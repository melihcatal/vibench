"""Run OCR on a stored document object in S3 using AWS Textract.

Uses boto3 to call the AWS Textract service (model: Textract AnalyzeDocument / DetectDocumentText)
to extract text from PDF or image objects stored in S3.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import io
from storage_client import get_textract_client, get_s3_client
from storage_models import OCRResult


TEXTRACT_MODEL_ID = "aws-textract-detect-text"


def _extract_text_from_blocks(blocks):
    """Extract readable text from Textract block list, joining LINE blocks."""
    lines = []
    for block in blocks:
        if block["BlockType"] == "LINE":
            lines.append(block["Text"])
    return " ".join(lines)


def _compute_avg_confidence(blocks):
    """Compute average confidence score across all LINE blocks."""
    confidences = [
        block["Confidence"]
        for block in blocks
        if block["BlockType"] == "LINE" and "Confidence" in block
    ]
    if not confidences:
        return None
    return sum(confidences) / len(confidences)


def stored_document_ocr(bucket, key, region=None, s3_endpoint_url=None):
    """Run OCR on a document stored in S3 using AWS Tetect.

    Calls Textract DetectDocumentText API on the S3 object. Supports
    PDF (single-page) and image formats (PNG, JPEG).

    Args:
        bucket: S3 bucket name.
        key: S3 object key of the document.
        region: Optional AWS region override.
        s3_endpoint_url: Optional custom S3 endpoint.

    Returns:
        OCRResult containing extracted text, blocks, confidence, and page info.

    Raises:
        botocore.exceptions.ClientError: If Textract fails (e.g., unsupported format).
    """
    textract_client = get_textract_client(region=region)

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        }
    )

    blocks = response.get("Blocks", [])
    text = _extract_text_from_blocks(blocks)
    confidence = _compute_avg_confidence(blocks)

    pages = []
    for block in blocks:
        if block["BlockType"] == "PAGE":
            pages.append({
                "page_number": block.get("Id"),
                "confidence": block.get("Confidence"),
            })

    return OCRResult(
        object_uri=f"s3://{bucket}/{key}",
        text=text,
        blocks=blocks,
        confidence=confidence,
        pages=pages,
    )


def stored_document_ocr_bytes(body, region=None):
    """Run OCR on document bytes using AWS Textract.

    Useful when the document has already been downloaded from S3 or
    originates from another source.

    Args:
        body: Bytes of the document (PNG, JPEG, or PDF).
        region: Optional AWS region override.

    Returns:
        OCRResult containing extracted text, blocks, and confidence.
    """
    textract_client = get_textract_client(region=region)

    response = textract_client.detect_document_text(
        Document={"Bytes": body}
    )

    blocks = response.get("Blocks", [])
    text = _extract_text_from_blocks(blocks)
    confidence = _compute_avg_confidence(blocks)

    return OCRResult(
        object_uri="in-memory",
        text=text,
        blocks=blocks,
        confidence=confidence,
        pages=[],
    )
