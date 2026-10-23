"""
Extract table cells and row structure from a document using AWS Textract.

Uses the TABLES feature of AWS Textract AnalyzeDocument API to identify
tables and extract their cell contents with row/column structure.
"""

import os
from typing import Optional, List

import boto3
from botocore.exceptions import ClientError

from document_client import (
    get_textract_client,
    prepare_textract_document,
    load_image_as_bytes,
    validate_image_size,
)
from document_models import (
    TableResult,
    ExtractedTable,
    TableRow,
    TableCell,
    normalize_textract_table,
)


# AWS Textract service and feature identifiers
TEXTRACT_SERVICE_NAME = "textract"
TEXTRACT_ANALYZE_DOCUMENT_API = "analyze_document"
TEXTRACT_TABLES_FEATURE = "TABLES"


def extract_tables_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> TableResult:
    """
    Extract tables from a document image using AWS Textract.
    
    This function uses the AWS Textract AnalyzeDocument API with the
    TABLES feature type to identify tables in the document and extract
    their cell contents with row/column structure.
    
    Args:
        image_path: Path to the image file (PNG, JPEG, TIFF).
        image_bytes: Raw image bytes (alternative to image_path).
        
    Returns:
        TableResult: Container with extracted tables and metadata.
        
    Raises:
        ValueError: If neither image_path nor image_bytes is provided.
        ClientError: If AWS Textract API call fails.
    """
    if image_bytes is None:
        if image_path is None:
            raise ValueError("Either image_path or image_bytes must be provided")
        image_bytes = load_image_as_bytes(image_path)
    
    if not validate_image_size(image_bytes):
        raise ValueError("Image exceeds 5MB limit for AWS Textract sync API")
    
    client = get_textract_client()
    document = prepare_textract_document(image_bytes)
    
    try:
        response = client.analyze_document(
            Document=document,
            FeatureTypes=[TEXTRACT_TABLES_FEATURE],
        )
    except ClientError as e:
        raise ClientError(
            e.response["Error"],
            f"Textract.{TEXTRACT_ANALYZE_DOCUMENT_API}",
        ) from e
    
    raw_blocks = response.get("Blocks", [])
    table_blocks = [b for b in raw_blocks if b.get("BlockType") == "TABLE"]
    
    extracted_tables = []
    for table_block in table_blocks:
        table = normalize_textract_table(table_block, raw_blocks)
        extracted_tables.append(table)
    
    page_count = len([b for b in raw_blocks if b.get("BlockType") == "PAGE"])
    
    return TableResult(
        tables=extracted_tables,
        pages=max(page_count, 1),
    )


def extract_tables_from_bytes(image_bytes: bytes) -> List[ExtractedTable]:
    """
    Convenience function to extract tables from image bytes.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        List[ExtractedTable]: Extracted tables.
    """
    result = extract_tables_from_image(image_bytes=image_bytes)
    return result.tables


def extract_tables_from_file(image_path: str) -> List[ExtractedTable]:
    """
    Convenience function to extract tables from a file.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[ExtractedTable]: Extracted tables.
    """
    result = extract_tables_from_image(image_path=image_path)
    return result.tables


def get_table_as_dicts(image_path: str) -> List[List[dict]]:
    """
    Extract tables and return them as list of row dictionaries.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[List[dict]]: Tables represented as lists of row dicts.
    """
    result = extract_tables_from_image(image_path=image_path)
    tables_as_dicts = []
    
    for table in result.tables:
        if not table.rows:
            continue
        
        headers = []
        for cell in table.rows[0].cells:
            headers.append(cell.get("text", ""))
        
        rows_as_dicts = []
        for row in table.rows[1:]:
            row_dict = {}
            for cell in row.cells:
                col_idx = cell.get("col_index", 0)
                if col_idx < len(headers):
                    row_dict[headers[col_idx]] = cell.get("text", "")
                else:
                    row_dict[f"column_{col_idx}"] = cell.get("text", "")
            rows_as_dicts.append(row_dict)
        
        tables_as_dicts.append(rows_as_dicts)
    
    return tables_as_dicts


def get_table_as_csv(table: ExtractedTable) -> str:
    """
    Convert a single extracted table to CSV format.
    
    Args:
        table: ExtractedTable object.
        
    Returns:
        str: CSV representation of the table.
    """
    lines = []
    for row in table.rows:
        cells = sorted(row.cells, key=lambda c: c.get("col_index", 0))
        values = [c.get("text", "").replace(",", ";").replace("\n", " ") for c in cells]
        lines.append(",".join(values))
    return "\n".join(lines)


def get_table_count(image_path: str) -> int:
    """
    Count the number of tables in a document.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        int: Number of tables detected.
    """
    result = extract_tables_from_image(image_path=image_path)
    return len(result.tables)
