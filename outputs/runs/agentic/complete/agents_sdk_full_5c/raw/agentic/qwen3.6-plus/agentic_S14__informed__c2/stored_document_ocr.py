"""
stored_document_ocr.py - Run OCR on a stored document object in Amazon S3
using Amazon Textract.

Uses the boto3 SDK (Amazon Textract).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import create_s3_client, handle_s3_error
from storage_models import OcrRequest, OcrResponse, parse_textract_response


def stored_document_ocr(
    bucket: str,
    key: str,
    document_type: str = "ANALYSIS",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> OcrResponse:
    """
    Run OCR (Optical Character Recognition) on a document stored in Amazon S3
    using Amazon Textract.

    Amazon Textract automatically detects and extracts printed and handwritten
    text, tables, and structured data from scanned documents.

    Args:
        bucket: S3 bucket name containing the document.
        key: Object key (path) of the document in S3.
        document_type: "ANALYSIS" for full analysis (forms, tables, text) or
                       "DETECTION" for basic text detection only.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override (Textract region must support the API).

    Returns:
        OcrResponse with extracted text, blocks, pages, and confidence score.
    """
    request = OcrRequest(
        bucket=bucket,
        key=key,
        document_type=document_type,
    )

    # Create Textract client via boto3
    textract_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    textract_client = boto3.client(
        "textract",
        region_name=textract_region,
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    )

    document_location = {
        "S3Object": {
            "Bucket": request.bucket,
            "Name": request.key,
        }
    }

    try:
        if request.document_type == "ANALYSIS":
            # Amazon Textract AnalyzeDocument API: extracts text, forms, tables, key-values
            response = textract_client.analyze_document(
                Document={"S3Object": document_location["S3Object"]},
                FeatureTypes=["TABLES", "FORMS", "SIGNATURES"],
            )
        else:
            # Amazon Textract DetectDocumentText API: basic text detection
            response = textract_client.detect_document_text(
                Document={"S3Object": document_location["S3Object"]},
            )

        # Parse the Textract response using our helper
        parsed = parse_textract_response(response)

        # Calculate average confidence score
        blocks = parsed.get("blocks", [])
        if blocks:
            avg_confidence = sum(b.get("confidence", 0) for b in blocks) / len(blocks)
        else:
            avg_confidence = 0.0

        pages_count = len(parsed.get("pages", []))

        return OcrResponse(
            bucket=request.bucket,
            key=request.key,
            text=parsed["text"],
            blocks=parsed["blocks"],
            pages=parsed["pages"],
            pages_count=pages_count,
            confidence_score=round(avg_confidence, 2),
        )

    except ClientError as e:
        error_msg = handle_s3_error(e, "stored_document_ocr")
        return OcrResponse(
            bucket=request.bucket,
            key=request.key,
            text="",
            blocks=[],
            pages=[],
            pages_count=0,
            confidence_score=0.0,
        )
