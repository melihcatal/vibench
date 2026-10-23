"""
stored_document_ocr.py — Run OCR on a stored document object.

Concrete provider: Amazon Textract via boto3 SDK.
Provider signals:
  - boto3 Textract client creation ("textract")
  - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars
  - detect_document_text / analyze_document API calls
"""

import os
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

import boto3
from upload_object import upload_object
from object_metadata import get_object_metadata


def _download_s3_object_to_bytes(bucket: str, key: str) -> bytes:
    """Fetch an S3 object's raw bytes for OCR processing."""
    client = boto3.client("s3")
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def run_ocr_on_stored_document(
    source_bucket: str,
    source_key: str,
    model: str = "detect_document_text",
) -> Dict:
    """
    Run Amazon Textract OCR on a document stored in S3.

    Supports two modes:
      - "detect_document_text": lightweight text detection (lines, words).
      - "analyze_document": full analysis including forms and tables.

    Parameters
    ----------
    source_bucket : str
        S3 bucket containing the document.
    source_key : str
        S3 key of the document (PDF, PNG, JPEG, TIFF).
    model : str
        Textract operation mode. Options: "detect_document_text", "analyze_document".

    Returns
    -------
    dict
        Normalized OCR result with extracted text, lines, tables, and key-value pairs.

    Raises
    ------
    ClientError
        When Textract fails (unsupported format, permissions, etc.).
    """
    textract_client = boto3.client("textract")

    # Use S3 reference mode for Textract (no need to download if in same region)
    document_location = {
        "S3Object": {
            "Bucket": source_bucket,
            "Name": source_key,
        }
    }

    if model == "analyze_document":
        response = textract_client.analyze_document(
            Document=document_location,
            FeatureTypes=["TABLES", "FORMS"],
        )
        return _normalize_analyze_document(response)
    else:
        response = textract_client.detect_document_text(
            Document=document_location,
        )
        return _normalize_detect_text(response)


def _normalize_detect_text(response: Dict) -> Dict:
    """Normalize Textract detect_document_text output."""
    full_text = []
    lines = []
    words = []

    for block in response.get("Blocks", []):
        block_type = block["BlockType"]
        text = block.get("Text", "")

        if block_type == "LINE":
            lines.append(text)
            full_text.append(text)
        elif block_type == "WORD":
            words.append({
                "text": text,
                "confidence": block.get("Confidence", 0),
            })

    return {
        "full_text": " ".join(full_text),
        "lines": lines,
        "words": words,
        "page_count": len([b for b in response.get("Blocks", []) if b.get("BlockType") == "PAGE"]),
        "service": "Amazon Textract",
        "model": "detect_document_text",
    }


def _normalize_analyze_document(response: Dict) -> Dict:
    """Normalize Textract analyze_document output."""
    full_text = []
    lines = []
    tables = []
    key_value_pairs = {}

    for block in response.get("Blocks", []):
        block_type = block["BlockType"]
        text = block.get("Text", "")

        if block_type == "LINE":
            lines.append(text)
            full_text.append(text)
        elif block_type == "TABLE":
            table_id = block.get("Id", "")
            tables.append({"id": table_id, "confidence": block.get("Confidence", 0)})
        elif block_type == "KEY_VALUE_SET":
            entity_types = block.get("EntityTypes", [])
            if "KEY" in entity_types:
                # Collect key text from child blocks
                key_text = _get_block_text(block, response)
                key_value_pairs[key_text] = {"key": key_text, "value": None}
            elif "VALUE" in entity_types:
                value_text = _get_block_text(block, response)
                # Attach to most recent key
                if key_value_pairs:
                    last_key = list(key_value_pairs.keys())[-1]
                    key_value_pairs[last_key]["value"] = value_text

    return {
        "full_text": " ".join(full_text),
        "lines": lines,
        "tables": tables,
        "key_value_pairs": key_value_pairs,
        "page_count": len([b for b in response.get("Blocks", []) if b.get("BlockType") == "PAGE"]),
        "service": "Amazon Textract",
        "model": "analyze_document",
    }


def _get_block_text(block: Dict, response: Dict) -> str:
    """Extract text from a Textract block by following relationships."""
    texts = []
    for rel in block.get("Relationships", []):
        if rel["Type"] == "CHILD":
            for child_id in rel["Ids"]:
                for b in response.get("Blocks", []):
                    if b["Id"] == child_id:
                        texts.append(b.get("Text", ""))
    return " ".join(texts)
