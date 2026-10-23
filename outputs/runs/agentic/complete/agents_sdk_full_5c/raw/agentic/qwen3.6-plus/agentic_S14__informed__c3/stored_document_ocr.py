"""
Run OCR on a stored document object using Amazon Textract.

Uses boto3 SDK for Amazon Textract (service=Amazon Textract).
Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import io
from typing import List, Optional

import boto3

from storage_client import get_s3_client
from storage_models import ObjectMetadataResponse
from object_metadata import get_object_metadata


def _build_s3_object_ref(bucket: str, object_key: str) -> dict:
    """Build S3 object reference dict for Textract API calls."""
    return {
        "S3Object": {
            "Bucket": bucket,
            "Name": object_key,
        }
    }


def _extract_text_from_blocks(blocks: List[dict]) -> str:
    """
    Extract plain text from Textract response blocks.
    Filters for LINE blocks and joins their text.
    """
    lines = []
    for block in blocks:
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))
    return "\n".join(lines)


def run_ocr_on_stored_document(
    bucket: str,
    object_key: str,
    prefix: Optional[str] = None,
    feature_types: Optional[List[str]] = None,
) -> dict:
    """
    Run OCR on a stored document in Amazon S3 using Amazon Textract.

    Supports text detection, table extraction, form extraction, and layout analysis.

    Args:
        bucket: The S3 bucket containing the document.
        object_key: The S3 object key of the document.
        prefix: Optional prefix to prepend to the object key.
        feature_types: Optional list of Textract features:
            - "TABLES" - extract tabular data
            - "FORMS" - extract key-value pairs from forms
            - "LAYOUT" - extract document layout elements
            - "SIGNATURES" - detect signatures

    Returns:
        dict with keys:
            - text: Extracted plain text from the document
            - blocks: Raw Textract response blocks
            - pages: Number of pages processed
            - tables: List of extracted tables (if TABLES feature used)
            - forms: List of extracted form key-value pairs (if FORMS feature used)

    Raises:
        ValueError: If the document is not a supported format.
        ClientError: On Textract or S3 API errors.
    """
    if prefix:
        object_key = f"{prefix.rstrip('/')}/{object_key.lstrip('/')}"

    metadata = get_object_metadata(bucket, object_key)
    if metadata is None:
        raise FileNotFoundError(
            f"Object s3://{bucket}/{object_key} not found"
        )

    supported_types = {
        "image/png",
        "image/jpeg",
        "application/pdf",
        "image/tiff",
    }
    if metadata.content_type and metadata.content_type not in supported_types:
        raise ValueError(
            f"Unsupported document content type: {metadata.content_type}. "
            f"Supported types: {supported_types}"
        )

    textract_client = boto3.client("textract")

    api_kwargs = {
        "Document": _build_s3_object_ref(bucket, object_key),
    }

    if feature_types:
        api_kwargs["FeatureTypes"] = feature_types
        detect_method = textract_client.analyze_document
    else:
        detect_method = textract_client.detect_document_text

    response = detect_method(**api_kwargs)

    result = {
        "text": _extract_text_from_blocks(response.get("Blocks", [])),
        "blocks": response.get("Blocks", []),
        "pages": 1,
        "tables": [],
        "forms": [],
    }

    if response.get("Blocks"):
        for block in response["Blocks"]:
            if block.get("BlockType") == "PAGE":
                pass
            if block.get("BlockType") == "TABLE" and feature_types and "TABLES" in feature_types:
                result["tables"].append(_extract_table_data(response["Blocks"], block["Id"]))
            if block.get("BlockType") == "KEY_VALUE_SET" and feature_types and "FORMS" in feature_types:
                if "KEY" in block.get("EntityTypes", []):
                    kv = _extract_form_pair(response["Blocks"], block)
                    if kv:
                        result["forms"].append(kv)

    return result


def _extract_table_data(blocks: List[dict], table_id: str) -> List[List[str]]:
    """Extract a table as a 2D list of cell values from Textract blocks."""
    cell_map = {}
    for block in blocks:
        if block.get("BlockType") == "CELL" and table_id in block.get("Relationships", [{}])[0].get("Ids", []):
            row = block.get("RowIndex", 1)
            col = block.get("ColumnIndex", 1)
            text = ""
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        for b in blocks:
                            if b["Id"] == child_id and b["BlockType"] == "WORD":
                                text += b.get("Text", "") + " "
            cell_map[(row, col)] = text.strip()

    if not cell_map:
        return []

    max_row = max(r for r, _ in cell_map.keys())
    max_col = max(c for _, c in cell_map.keys())

    table = []
    for r in range(1, max_row + 1):
        row = []
        for c in range(1, max_col + 1):
            row.append(cell_map.get((r, c), ""))
        table.append(row)
    return table


def _extract_form_pair(blocks: List[dict], key_block: dict) -> Optional[dict]:
    """Extract a form key-value pair from Textract blocks."""
    key_text = _get_text_for_block(blocks, key_block["Id"])
    value_block_ids = []
    for rel in key_block.get("Relationships", []):
        if rel["Type"] == "VALUE":
            value_block_ids.extend(rel["Ids"])

    if not value_block_ids:
        return None

    value_text_parts = []
    for vid in value_block_ids:
        for b in blocks:
            if b["Id"] == vid and b["BlockType"] in ("WORD", "SELECTION_ELEMENT"):
                value_text_parts.append(b.get("Text", ""))

    return {
        "key": key_text.strip(),
        "value": " ".join(value_text_parts).strip(),
    }


def _get_text_for_block(blocks: List[dict], block_id: str) -> str:
    """Get text content associated with a block by traversing child relationships."""
    text_parts = []
    for block in blocks:
        if block["Id"] == block_id:
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        for b in blocks:
                            if b["Id"] == child_id and b["BlockType"] == "WORD":
                                text_parts.append(b.get("Text", ""))
    return " ".join(text_parts)
