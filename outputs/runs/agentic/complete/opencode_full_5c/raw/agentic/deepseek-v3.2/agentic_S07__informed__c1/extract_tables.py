import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import TableResult, TableCell, TextractBlock, BlockType


def extract_tables_from_image(
    image_path: str, region: Optional[str] = None
) -> List[TableResult]:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    features = client.get_textract_features("tables")
    request["FeatureTypes"] = features

    response = textract_client.analyze_document(**request)

    return parse_tables_from_response(response)


def parse_tables_from_response(response: Dict[str, Any]) -> List[TableResult]:
    blocks = {}
    tables = []

    for block_data in response.get("Blocks", []):
        block = TextractBlock.from_aws_response(block_data)
        blocks[block.id] = block

        if block.block_type == BlockType.TABLE:
            table_result = extract_table_structure(block, blocks)
            if table_result:
                tables.append(table_result)

    return tables


def extract_table_structure(
    table_block: TextractBlock, all_blocks: Dict[str, TextractBlock]
) -> Optional[TableResult]:
    if not table_block.relationships:
        return None

    cells = []
    max_row = 0
    max_col = 0

    for relationship in table_block.relationships:
        if relationship.get("Type") == "CHILD":
            for cell_id in relationship.get("Ids", []):
                cell_block = all_blocks.get(cell_id)
                if cell_block and cell_block.block_type == BlockType.CELL:
                    cell_info = extract_cell_info(cell_block, all_blocks)
                    if cell_info:
                        cells.append(cell_info)
                        max_row = max(max_row, cell_info.row_index + 1)
                        max_col = max(max_col, cell_info.column_index + 1)

    return TableResult(
        table_id=table_block.id, cells=cells, rows=max_row, columns=max_col
    )


def extract_cell_info(
    cell_block: TextractBlock, all_blocks: Dict[str, TextractBlock]
) -> Optional[TableCell]:
    row_index = cell_block.entity_types and "ROW" in cell_block.entity_types
    col_index = cell_block.entity_types and "COLUMN" in cell_block.entity_types

    if not row_index or not col_index:
        return None

    row_idx = (
        cell_block.entity_types.index("ROW") if "ROW" in cell_block.entity_types else -1
    )
    col_idx = (
        cell_block.entity_types.index("COLUMN")
        if "COLUMN" in cell_block.entity_types
        else -1
    )

    cell_text = ""
    if cell_block.relationships:
        for relationship in cell_block.relationships:
            if relationship.get("Type") == "CHILD":
                for child_id in relationship.get("Ids", []):
                    child_block = all_blocks.get(child_id)
                    if (
                        child_block
                        and child_block.block_type == BlockType.WORD
                        and child_block.text
                    ):
                        cell_text += child_block.text + " "

    return TableCell(
        row_index=row_idx,
        column_index=col_idx,
        text=cell_text.strip(),
        confidence=cell_block.confidence or 0.0,
    )


def extract_tables_as_dataframes(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    tables = extract_tables_from_image(image_path, region)

    table_data = []
    for i, table in enumerate(tables):
        table_dict = {
            "table_id": table.table_id,
            "rows": table.rows,
            "columns": table.columns,
            "data": table.to_list_of_lists(),
            "cells": [
                {
                    "row": cell.row_index,
                    "column": cell.column_index,
                    "text": cell.text,
                    "confidence": cell.confidence,
                }
                for cell in table.cells
            ],
        }
        table_data.append(table_dict)

    return table_data
