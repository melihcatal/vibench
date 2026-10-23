import boto3
import os
import base64
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError
from storage_client import get_s3_client, get_textract_client
from storage_models import OCRResult


def extract_text_from_s3_document(bucket_name: str, object_key: str) -> OCRResult:
    """
    Run OCR on a document stored in S3 using Amazon Textract.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: S3 object key of the document

    Returns:
        OCRResult with extracted text and metadata
    """
    textract_client = get_textract_client()

    try:
        # Call Textract for document text detection
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
        )

        # Extract text from blocks
        extracted_text = ""
        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"

        # Calculate average confidence
        line_blocks = [
            b for b in response.get("Blocks", []) if b["BlockType"] == "LINE"
        ]
        if line_blocks:
            avg_confidence = sum(b.get("Confidence", 0) for b in line_blocks) / len(
                line_blocks
            )
        else:
            avg_confidence = 0.0

        return OCRResult(
            success=True,
            text=extracted_text.strip(),
            pages=[{"blocks": response.get("Blocks", [])}],
            confidence=avg_confidence,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return OCRResult(
            success=False, error=f"Textract error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return OCRResult(success=False, error=f"Unexpected error: {str(e)}")


def extract_text_from_bytes(document_bytes: bytes) -> OCRResult:
    """
    Run OCR on document bytes using Amazon Textract.

    Args:
        document_bytes: Document content as bytes

    Returns:
        OCRResult with extracted text and metadata
    """
    textract_client = get_textract_client()

    try:
        # Encode bytes as base64 for Textract
        document_base64 = base64.b64encode(document_bytes).decode("utf-8")

        response = textract_client.detect_document_text(
            Document={"Bytes": document_bytes}
        )

        # Extract text from blocks
        extracted_text = ""
        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"

        # Calculate average confidence
        line_blocks = [
            b for b in response.get("Blocks", []) if b["BlockType"] == "LINE"
        ]
        if line_blocks:
            avg_confidence = sum(b.get("Confidence", 0) for b in line_blocks) / len(
                line_blocks
            )
        else:
            avg_confidence = 0.0

        return OCRResult(
            success=True,
            text=extracted_text.strip(),
            pages=[{"blocks": response.get("Blocks", [])}],
            confidence=avg_confidence,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return OCRResult(
            success=False, error=f"Textract error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return OCRResult(success=False, error=f"Unexpected error: {str(e)}")


def analyze_document_layout(bucket_name: str, object_key: str) -> Dict[str, Any]:
    """
    Analyze document layout including forms and tables.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: S3 object key of the document

    Returns:
        Dictionary with layout analysis results
    """
    textract_client = get_textract_client()

    try:
        response = textract_client.analyze_document(
            Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
            FeatureTypes=["FORMS", "TABLES"],
        )

        # Process blocks by type
        blocks_by_type = {}
        for block in response.get("Blocks", []):
            block_type = block["BlockType"]
            if block_type not in blocks_by_type:
                blocks_by_type[block_type] = []
            blocks_by_type[block_type].append(block)

        return {
            "success": True,
            "blocks_by_type": blocks_by_type,
            "total_blocks": len(response.get("Blocks", [])),
            "has_forms": "KEY_VALUE_SET" in blocks_by_type,
            "has_tables": "TABLE" in blocks_by_type,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return {
            "success": False,
            "error": f"Textract error ({error_code}): {error_msg}",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
