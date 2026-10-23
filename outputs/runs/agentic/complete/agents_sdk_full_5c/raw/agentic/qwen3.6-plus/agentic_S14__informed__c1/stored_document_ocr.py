"""
Run OCR on a stored document object in Amazon S3 using Amazon Textract.

Downloads the document object from Amazon S3 and submits it to the
Amazon Textract service for text detection and layout analysis.
Credentials are resolved from AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
or the default AWS credential chain.
"""

from __future__ import annotations

import io
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import create_s3_client
from storage_models import ocr_extraction_result_to_text

logger = logging.getLogger(__name__)

# Amazon Textract model/feature identifiers
TEXTRACT_DETECT_TEXT = "DetectDocumentText"
TEXTRACT_ANALYZE_DOCUMENT = "AnalyzeDocument"
TEXTRACT_FEATURES_FORMS = ["FORMS"]
TEXTRACT_FEATURES_TABLES = ["TABLES"]
TEXTRACT_FEATURES_QUERIES = ["QUERIES"]
TEXTRACT_FEATURES_ALL = ["FORMS", "TABLES", "SIGNATURES"]


def detect_text_from_s3(
    bucket: str,
    key: str,
    *,
    s3_client: Optional[boto3.client] = None,
    textract_client: Optional[boto3.client] = None,
) -> dict:
    """
    Detect text in a document stored in Amazon S3 using Amazon Textract.

    Uses the DetectDocumentText API which returns all detected words and
    lines with bounding boxes and confidence scores.

    Args:
        bucket: S3 bucket containing the document.
        key: Object key of the document.
        s3_client: Optional pre-created boto3 S3 client.
        textract_client: Optional pre-created boto3 Textract client.

    Returns:
        Raw Textract DetectDocumentText response as a dict.
    """
    if textract_client is None:
        textract_client = boto3.client("textract")

    try:
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key,
                }
            }
        )
    except ClientError as exc:
        logger.error(
            "Amazon Textract DetectDocumentText failed for s3://%s/%s: %s",
            bucket,
            key,
            exc,
        )
        raise

    logger.info(
        "Amazon Textract detected %d blocks for s3://%s/%s",
        len(response.get("Blocks", [])),
        bucket,
        key,
    )
    return response


def analyze_document_from_s3(
    bucket: str,
    key: str,
    *,
    feature_types: Optional[list[str]] = None,
    s3_client: Optional[boto3.client] = None,
    textract_client: Optional[boto3.client] = None,
) -> dict:
    """
    Analyze a document stored in Amazon S3 using Amazon Textract.

    Uses the AnalyzeDocument API to extract text, forms, tables,
    and signatures depending on requested feature types.

    Args:
        bucket: S3 bucket containing the document.
        key: Object key of the document.
        feature_types: List of features to analyze (FORMS, TABLES, SIGNATURES).
        s3_client: Optional pre-created boto3 S3 client.
        textract_client: Optional pre-created boto3 Textract client.

    Returns:
        Raw Textract AnalyzeDocument response as a dict.
    """
    if textract_client is None:
        textract_client = boto3.client("textract")

    features = feature_types or TEXTRACT_FEATURES_ALL

    try:
        response = textract_client.analyze_document(
            Document={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key,
                }
            },
            FeatureTypes=features,
        )
    except ClientError as exc:
        logger.error(
            "Amazon Textract AnalyzeDocument failed for s3://%s/%s: %s",
            bucket,
            key,
            exc,
        )
        raise

    logger.info(
        "Amazon Textract analyzed %d blocks for s3://%s/%s with features %s",
        len(response.get("Blocks", [])),
        bucket,
        key,
        features,
    )
    return response


def ocr_document_from_s3_bytes(
    bucket: str,
    key: str,
    *,
    feature_types: Optional[list[str]] = None,
    s3_client: Optional[boto3.client] = None,
    textract_client: Optional[boto3.client] = None,
) -> dict:
    """
    Download a document from S3 and run OCR using Amazon Textract via bytes upload.

    Useful when the document is not directly accessible to Textract from S3
    (e.g., different AWS accounts, private VPC endpoints).

    Args:
        bucket: S3 bucket containing the document.
        key: Object key of the document.
        feature_types: Features to analyze (FORMS, TABLES, SIGNATURES).
        s3_client: Optional pre-created boto3 S3 client.
        textract_client: Optional pre-created boto3 Textract client.

    Returns:
        Raw Textract AnalyzeDocument response as a dict.
    """
    if s3_client is None:
        s3_client = create_s3_client()
    if textract_client is None:
        textract_client = boto3.client("textract")

    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        document_bytes = obj["Body"].read()
    except ClientError as exc:
        logger.error("Failed to download s3://%s/%s from S3: %s", bucket, key, exc)
        raise

    features = feature_types or TEXTRACT_FEATURES_ALL

    try:
        response = textract_client.analyze_document(
            Document={"Bytes": document_bytes},
            FeatureTypes=features,
        )
    except ClientError as exc:
        logger.error(
            "Amazon Textract AnalyzeDocument (bytes) failed for s3://%s/%s: %s",
            bucket,
            key,
            exc,
        )
        raise

    return response


def extract_text_from_textract_response(response: dict) -> str:
    """
    Extract plain text from an Amazon Textract response.

    Args:
        response: Raw Textract response dict.

    Returns:
        Plain text string with detected lines joined by newlines.
    """
    return ocr_extraction_result_to_text(response)


def get_full_text_from_s3(
    bucket: str,
    key: str,
    *,
    s3_client: Optional[boto3.client] = None,
    textract_client: Optional[boto3.client] = None,
) -> str:
    """
    High-level convenience function: detect text from S3 document and return plain text.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        s3_client: Optional pre-created boto3 S3 client.
        textract_client: Optional pre-created boto3 Textract client.

    Returns:
        Extracted plain text from the document.
    """
    response = detect_text_from_s3(
        bucket, key, s3_client=s3_client, textract_client=textract_client
    )
    return extract_text_from_textract_response(response)
