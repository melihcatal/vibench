"""
Run OCR on a stored document object.

Uses AWS Textract as the concrete managed OCR service.
Reads documents from S3 and extracts text, tables, and structural elements.
"""

import io
import json
from typing import Any, Dict, List, Optional, Union

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient, get_client


# AWS Textract concrete model / API identifiers
TEXTRACT_DOCUMENT_DETECTION_MODEL = "AWS_Textract_AnalyzeDocument"
TEXTRACT_OCR_API_ENDPOINT = "textract"


class TextractOCRResult:
    """Structured result from AWS Textract OCR processing."""

    def __init__(self, response: Dict[str, Any]):
        self.raw_response = response
        self.blocks = response.get("Blocks", [])
        self.detect_document_text = self._extract_text()
        self.detect_tables = self._extract_tables()
        self.detect_forms = self._extract_forms()
        self.detect_key_value_pairs = self._extract_key_values()
        self.pages = self._extract_pages()
        self.document_metadata = response.get("DocumentMetadata", {})
        self.job_id = response.get("JobId")
        self.model_version = response.get("DocumentMetadata", {}).get(
            "Pages", 0
        )

    def _extract_text(self) -> str:
        """Extract plain text from Textract LINE blocks."""
        lines = []
        for block in self.blocks:
            if block.get("BlockType") == "LINE":
                lines.append(block.get("Text", ""))
        return "\n".join(lines)

    def _extract_tables(self) -> List[List[List[str]]]:
        """Extract table data from Textract TABLE and CELL blocks."""
        tables = []
        current_table_cells = {}
        current_table_id = None

        for block in self.blocks:
            if block["BlockType"] == "TABLE":
                if current_table_id is not None and current_table_cells:
                    tables.append(self._build_table(current_table_cells))
                current_table_id = block["Id"]
                current_table_cells = {}
            elif block["BlockType"] == "CELL" and current_table_id:
                row_idx = block.get("RowIndex", 0)
                col_idx = block.get("ColumnIndex", 0)
                current_table_cells[(row_idx, col_idx)] = block.get("Text", "")

        if current_table_id is not None and current_table_cells:
            tables.append(self._build_table(current_table_cells))

        return tables

    def _build_table(self, cells: Dict[tuple, str]) -> List[List[str]]:
        """Build a 2D table from cell data."""
        if not cells:
            return []
        max_row = max(r for r, c in cells.keys())
        max_col = max(c for r, c in cells.keys())
        table = []
        for r in range(1, max_row + 1):
            row = []
            for c in range(1, max_col + 1):
                row.append(cells.get((r, c), ""))
            table.append(row)
        return table

    def _extract_forms(self) -> Dict[str, str]:
        """Extract key-value form data from Textract blocks."""
        forms = {}
        for block in self.blocks:
            if block.get("BlockType") == "KEY_VALUE_SET":
                relationships = block.get("Relationships", [])
                key_text = ""
                value_text = ""
                for rel in relationships:
                    if rel.get("Type") == "CHILD":
                        child_ids = rel.get("Ids", [])
                        for cid in child_ids:
                            child_block = next(
                                (b for b in self.blocks if b["Id"] == cid),
                                None,
                            )
                            if child_block:
                                child_text = child_block.get("Text", "")
                                entity_types = block.get("EntityTypes", [])
                                if "KEY" in entity_types:
                                    key_text = child_text
                                elif "VALUE" in entity_types:
                                    value_text = child_text
                if key_text:
                    forms[key_text] = value_text
        return forms

    def _extract_key_values(self) -> List[Dict[str, Any]]:
        """Extract detailed key-value pairs with confidence scores."""
        key_values = []
        for block in self.blocks:
            if block.get("BlockType") == "KEY_VALUE_SET":
                entity_types = block.get("EntityTypes", [])
                kv = {
                    "type": entity_types,
                    "confidence": block.get("Confidence", 0),
                    "geometry": block.get("Geometry", {}),
                    "page": block.get("Page", 0),
                }
                key_values.append(kv)
        return key_values

    def _extract_pages(self) -> List[Dict[str, Any]]:
        """Extract page-level metadata."""
        pages = []
        for block in self.blocks:
            if block.get("BlockType") == "PAGE":
                pages.append(
                    {
                        "page_number": block.get("Page", 0),
                        "confidence": block.get("Confidence", 0),
                        "geometry": block.get("Geometry", {}),
                    }
                )
        return pages

    def get_full_text(self) -> str:
        """Return the complete extracted text."""
        return self.detect_document_text

    def to_dict(self) -> Dict[str, Any]:
        """Serialize result to dictionary."""
        return {
            "text": self.detect_document_text,
            "tables_count": len(self.detect_tables),
            "forms_count": len(self.detect_forms),
            "pages_count": len(self.pages),
            "metadata": self.document_metadata,
        }


def run_ocr_on_s3_object(
    bucket: str,
    key: str,
    feature_types: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
    storage_client: Optional[StorageClient] = None,
) -> TextractOCRResult:
    """
    Run AWS Textract OCR on a document stored in S3.

    Uses the S3 object reference directly with Textract's AnalyzeDocument API
    rather than downloading the file locally.

    Args:
        bucket: S3 bucket containing the document.
        key: S3 object key of the document.
        feature_types: Textract features to detect. Defaults to ["TABLES", "FORMS"].
        client_config: Optional boto3 client configuration overrides.
        storage_client: Optional pre-configured StorageClient.

    Returns:
        TextractOCRResult with extracted text, tables, and forms.

    Raises:
        ClientError: If Textract processing fails.
        UnsupportedDocumentException: If document format is not supported.
    """
    if feature_types is None:
        feature_types = ["TABLES", "FORMS"]

    textract_client = boto3.client(
        "textract",
        region_name=client_config.get("region_name") if client_config else None,
        endpoint_url=client_config.get("endpoint_url") if client_config else None,
    )

    document = {
        "S3Object": {
            "Bucket": bucket,
            "Name": key,
        }
    }

    try:
        response = textract_client.analyze_document(
            Document=document,
            FeatureTypes=feature_types,
        )
        return TextractOCRResult(response)

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        raise ClientError(
            e.response,
            f"Textract OCR failed for s3://{bucket}/{key}: {e} (code: {error_code})",
        )


def run_ocr_on_bytes(
    document_bytes: bytes,
    feature_types: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> TextractOCRResult:
    """
    Run AWS Textract OCR on in-memory document bytes.

    Args:
        document_bytes: Raw document bytes (PDF, PNG, JPEG, TIFF).
        feature_types: Textract features to detect.
        client_config: Optional boto3 client configuration overrides.

    Returns:
        TextractOCRResult with extracted content.
    """
    if feature_types is None:
        feature_types = ["TABLES", "FORMS"]

    textract_client = boto3.client(
        "textract",
        region_name=client_config.get("region_name") if client_config else None,
    )

    try:
        response = textract_client.analyze_document(
            Document={"Bytes": document_bytes},
            FeatureTypes=feature_types,
        )
        return TextractOCRResult(response)

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        raise ClientError(
            e.response,
            f"Textract OCR failed on byte content: {e} (code: {error_code})",
        )


def detect_document_text(
    bucket: str,
    key: str,
    client_config: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Quick text detection using AWS Textract DetectDocumentText API.

    Lighter-weight than AnalyzeDocument; returns only text lines and words.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        client_config: Optional client configuration.

    Returns:
        Extracted text as a string.
    """
    textract_client = boto3.client(
        "textract",
        region_name=client_config.get("region_name") if client_config else None,
    )

    document = {
        "S3Object": {
            "Bucket": bucket,
            "Name": key,
        }
    }

    try:
        response = textract_client.detect_document_text(Document=document)
        lines = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE":
                lines.append(block.get("Text", ""))
        return "\n".join(lines)

    except ClientError as e:
        raise ClientError(
            e.response,
            f"Textext text detection failed for s3://{bucket}/{key}: {e}",
        )
