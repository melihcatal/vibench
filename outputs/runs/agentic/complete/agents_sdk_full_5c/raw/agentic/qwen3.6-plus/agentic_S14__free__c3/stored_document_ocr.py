"""
Run OCR on a stored document object using AWS Textract.

Provider: AWS Textract via boto3
- Uses boto3.client('textract') for AWS Textract document analysis
- AWS Textract managed service for OCR on documents stored in S3
- AWS Textract DetectDocumentText API
"""

import base64
import logging
from typing import Dict, List, Optional, Tuple

from storage_client import get_s3_client, get_textract_client

logger = logging.getLogger(__name__)


def extract_document_text(
    bucket: str,
    key: str,
    use_s3_reference: bool = True,
) -> Dict:
    """
    Run OCR on a document stored in AWS S3 using AWS Textract.

    Supports both S3-reference mode (direct S3 object access by Textract)
    and inline byte mode for documents not in the same account.

    Provider signals:
    - boto3 Textract client (AWS Textract managed OCR service)
    - DetectDocumentText / AnalyzeDocument AWS Textract APIs
    - AWS Textract S3Object reference for direct S3 access
    """
    textract_client = get_textract_client()

    if use_s3_reference:
        logger.info(
            "Running AWS Textract OCR on s3://%s/%s via S3 reference",
            bucket, key,
        )
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key,
                }
            }
        )
    else:
        s3_client = get_s3_client()
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        document_bytes = obj["Body"].read()

        logger.info(
            "Running AWS Textract OCR on %d bytes from s3://%s/%s",
            len(document_bytes), bucket, key,
        )
        response = textract_client.detect_document_text(
            Document={
                "Bytes": document_bytes
            }
        )

    return response


def parse_textract_blocks(response: Dict) -> Tuple[str, List[Dict]]:
    """
    Parse AWS Textract response into plain text and structured blocks.

    Extracts LINE and WORD blocks from the Textract DetectDocumentText
    response and assembles readable text output.

    Provider signals:
    - AWS Textract block types: PAGE, LINE, WORD
    - AWS Textract response structure with Blocks array
    """
    blocks = response.get("Blocks", [])
    lines: List[Dict] = []
    line_texts: List[str] = []

    for block in blocks:
        if block.get("BlockType") == "LINE":
            text = block.get("Text", "")
            confidence = block.get("Confidence", 0.0)
            lines.append({
                "text": text,
                "confidence": confidence,
                "block_id": block.get("Id"),
                "geometry": block.get("Geometry"),
            })
            line_texts.append(text)

    full_text = "\n".join(line_texts)

    return full_text, lines


def ocr_stored_document(
    bucket: str,
    key: str,
    use_s3_reference: bool = True,
) -> Tuple[str, List[Dict]]:
    """
    End-to-end OCR: extract text from a stored document in AWS S3.

    Uses AWS Textract to detect document text and parses the results
    into readable text with line-level metadata.

    Provider signals:
    - AWS Textract DetectDocumentText API
    - AWS S3 + Textract integration via S3Object reference
    """
    response = extract_document_text(bucket, key, use_s3_reference)
    full_text, lines = parse_textract_blocks(response)

    logger.info(
        "AWS Textract OCR complete for s3://%s/%s: %d lines extracted",
        bucket, key, len(lines),
    )

    return full_text, lines
