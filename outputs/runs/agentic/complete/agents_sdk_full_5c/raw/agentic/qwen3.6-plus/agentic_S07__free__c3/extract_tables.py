"""
Extracts table cells and row structure from a document using AWS Textract.

Provider: AWS Textract (AnalyzeDocument API with TABLES feature)
Model/Feature: AWS Textract AnalyzeDocument with TABLES feature type
"""

import os
from typing import List

from document_client import (
    create_textract_client,
    load_image_bytes,
    build_textract_image_payload,
    normalize_textract_response,
)
from document_models import TableResponse, TableStructure, TableCell


# AWS Textract table extraction model identifier
TEXTRACT_TABLE_MODEL = "aws-textract-analyze-document-tables"

# Textract-specific block types for table processing
TABLE_BLOCK_TYPES = ["TABLE", "CELL", "COLUMN_HEADER", "SUM"]


def extract_tables_from_image(image_path: str) -> TableResponse:
    """
    Extract table structures from a document image using AWS Textract.

    Uses Textract's TABLES feature via AnalyzeDocument to detect tables
    and extract individual cells with row/column positioning.

    Args:
        image_path: Path to the document image file

    Returns:
        TableResponse containing all detected table structures
    """
    client = create_textract_client()
    image_bytes = load_image_bytes(image_path)
    payload = build_textract_image_payload(image_bytes)

    # AWS Textract AnalyzeDocument with TABLES feature
    response = client.analyze_document(
        Document=payload,
        FeatureTypes=["TABLES"]
    )

    normalized = normalize_textract_response(response)
    tables = _parse_tables(normalized["blocks"])

    page_blocks = [b for b in normalized["blocks"] if b.get("BlockType") == "PAGE"]
    page_count = max(len(page_blocks), 1)

    return TableResponse(
        tables=tables,
        page_count=page_count,
        model_version=normalized.get("model_version", TEXTRACT_TABLE_MODEL),
        status_code=normalized.get("status_code", 0),
    )


def _parse_tables(blocks: List[dict]) -> List[TableStructure]:
    """
    Parse Textract blocks into table structures with cells.

    Args:
        blocks: List of Textract Block dictionaries

    Returns:
        List of TableStructure objects
    """
    # Index all blocks by ID for relationship lookups
    block_index = {}
    for block in blocks:
        block_index[block.get("Id")] = block

    table_blocks = [b for b in blocks if b.get("BlockType") == "TABLE"]
    table_structures = []

    for table_block in table_blocks:
        cells = _extract_table_cells(table_block, block_index)

        # Calculate dimensions from cell positions
        max_row = max((c.row_index for c in cells), default=0)
        max_col = max((c.column_index for c in cells), default=0)

        structure = TableStructure(
            cells=cells,
            row_count=max_row + 1,
            column_count=max_col + 1,
            page=table_block.get("Page", 0),
            confidence=table_block.get("Confidence", 0.0),
        )
        table_structures.append(structure)

    return table_structures


def _extract_table_cells(table_block: dict, block_index: dict) -> List[TableCell]:
    """
    Extract individual cells from a Textract table block.

    Args:
        table_block: Textract TABLE block dictionary
        block_index: Dictionary mapping block IDs to blocks

    Returns:
        List of TableCell objects
    """
    cells = []
    relationships = table_block.get("Relationships", [])

    for rel in relationships:
        if rel.get("Type") != "CHILD":
            continue

        for cell_id in rel.get("Ids", []):
            cell_block = block_index.get(cell_id, {})
            if cell_block.get("BlockType") != "CELL":
                continue

            # Get cell text from child WORD blocks
            cell_text = _get_cell_text(cell_block, block_index)

            # Textract uses 1-based indexing for row/column
            row_index = cell_block.get("RowIndex", 1) - 1
            column_index = cell_block.get("ColumnIndex", 1) - 1
            row_span = cell_block.get("RowSpan", 1)
            column_span = cell_block.get("ColumnSpan", 1)

            # Check if cell is a column header (Textract-specific attribute)
            entity_types = cell_block.get("EntityTypes", [])
            is_header = "COLUMN_HEADER" in entity_types

            cell = TableCell(
                text=cell_text,
                row_index=row_index,
                column_index=column_index,
                is_header=is_header,
                confidence=cell_block.get("Confidence", 0.0),
                row_span=row_span,
                column_span=column_span,
            )
            cells.append(cell)

    return cells


def _get_cell_text(cell_block: dict, block_index: dict) -> str:
    """
    Extract text content from a Textract cell block.

    Args:
        cell_block: Textract CELL block dictionary
        block_index: Dictionary mapping block IDs to blocks

    Returns:
        Concatenated text from the cell
    """
    texts = []
    relationships = cell_block.get("Relationships", [])

    for rel in relationships:
        if rel.get("Type") == "CHILD":
            for child_id in rel.get("Ids", []):
                child = block_index.get(child_id, {})
                text = child.get("Text", "")
                if text:
                    texts.append(text)

    return " ".join(texts).strip()


def table_to_csv(table: TableStructure) -> str:
    """
    Convert a TableStructure to CSV format string.

    Args:
        table: TableStructure to convert

    Returns:
        CSV formatted string
    """
    import csv
    import io

    rows = {}
    for cell in table.cells:
        if cell.row_index not in rows:
            rows[cell.row_index] = {}
        rows[cell.row_index][cell.column_index] = cell.text

    output = io.StringIO()
    writer = csv.writer(output)
    for row_idx in sorted(rows.keys()):
        row = rows[row_idx]
        max_col = max(row.keys()) if row else 0
        csv_row = [row.get(col, "") for col in range(max_col + 1)]
        writer.writerow(csv_row)

    return output.getvalue()


def table_to_dict_list(table: TableStructure) -> List[dict]:
    """
    Convert a TableStructure to a list of dictionaries (header row as keys).

    Args:
        table: TableStructure to convert

    Returns:
        List of dictionaries, one per data row
    """
    rows = {}
    for cell in table.cells:
        if cell.row_index not in rows:
            rows[cell.row_index] = {}
        rows[cell.row_index][cell.column_index] = cell.text

    if not rows:
        return []

    header_row = rows.get(0, {})
    headers = [header_row.get(i, f"column_{i}") for i in range(table.column_count)]

    result = []
    for row_idx in sorted(rows.keys()):
        if row_idx == 0:
            continue
        row_data = rows[row_idx]
        record = {}
        for col_idx, header in enumerate(headers):
            record[header] = row_data.get(col_idx, "")
        result.append(record)

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_tables.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    result = extract_tables_from_image(img_path)

    print(f"Extracted {len(result.tables)} table(s) from {result.page_count} page(s)")
    for i, table in enumerate(result.tables):
        print(f"\nTable {i + 1} (Page {table.page}): {table.row_count} rows x {table.column_count} cols")
        print(table_to_csv(table))
