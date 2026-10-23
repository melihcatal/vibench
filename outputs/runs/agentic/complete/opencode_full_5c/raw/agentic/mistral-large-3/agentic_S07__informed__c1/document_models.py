from typing import Dict, List, Any


def normalize_textract_response(response: Dict) -> Dict:
    """
    Normalizes Amazon Textract response into a structured format.
    """
    blocks = response.get("Blocks", [])
    text = ""
    tables = []
    key_values = []
    layout_elements = []

    for block in blocks:
        if block["BlockType"] == "LINE":
            text += block["Text"] + "\n"
        elif block["BlockType"] == "TABLE":
            tables.append(_parse_table(block, blocks))
        elif block["BlockType"] == "KEY_VALUE_SET":
            if block["EntityTypes"][0] == "KEY":
                key_values.append(_parse_key_value(block, blocks))
        elif (
            block["BlockType"] == "LAYOUT_SECTION"
            or block["BlockType"] == "LAYOUT_HEADER"
            or block["BlockType"] == "LAYOUT_FOOTER"
        ):
            layout_elements.append(
                {
                    "type": block["BlockType"],
                    "text": block.get("Text", ""),
                    "geometry": block.get("Geometry", {}),
                }
            )

    return {
        "text": text.strip(),
        "tables": tables,
        "key_values": key_values,
        "layout_elements": layout_elements,
    }


def _parse_table(table_block: Dict, blocks: List[Dict]) -> Dict:
    """Parses a table block into a structured format."""
    rows = []
    relationships = table_block.get("Relationships", [])
    cell_ids = []

    for rel in relationships:
        if rel["Type"] == "CHILD":
            cell_ids.extend(rel["Ids"])

    cells = [block for block in blocks if block["Id"] in cell_ids]
    row_map = {}

    for cell in cells:
        row_index = cell["RowIndex"]
        if row_index not in row_map:
            row_map[row_index] = []
        row_map[row_index].append(
            {
                "text": cell.get("Text", ""),
                "row_index": cell["RowIndex"],
                "column_index": cell["ColumnIndex"],
            }
        )

    for row_index in sorted(row_map.keys()):
        rows.append(
            {"cells": sorted(row_map[row_index], key=lambda x: x["column_index"])}
        )

    return {"geometry": table_block.get("Geometry", {}), "rows": rows}


def _parse_key_value(key_block: Dict, blocks: List[Dict]) -> Dict:
    """Parses a key-value pair from blocks."""
    key_text = key_block.get("Text", "")
    value_text = ""
    relationships = key_block.get("Relationships", [])
    value_id = None

    for rel in relationships:
        if rel["Type"] == "VALUE":
            value_id = rel["Ids"][0]
            break

    if value_id:
        value_block = next((block for block in blocks if block["Id"] == value_id), None)
        if value_block:
            value_text = value_block.get("Text", "")

    return {
        "key": key_text,
        "value": value_text,
        "geometry": key_block.get("Geometry", {}),
    }
