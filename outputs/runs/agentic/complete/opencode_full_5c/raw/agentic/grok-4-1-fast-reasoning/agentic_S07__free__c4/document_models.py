from typing import List, Dict, Any


def parse_ocr_text(blocks: List[Dict[str, Any]]) -> List[str]:
    return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]


def normalize_block(block: Dict[str, Any]) -> Dict[str, Any]:
    bbox = block["Geometry"]["BoundingBox"]
    return {
        "id": block["Id"],
        "text": block.get("Text", ""),
        "block_type": block["BlockType"],
        "confidence": block.get("Confidence", 0.0),
        "bbox": {
            "left": bbox["Left"],
            "top": bbox["Top"],
            "width": bbox["Width"],
            "height": bbox["Height"],
        },
    }


def parse_layout_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        normalize_block(block)
        for block in blocks
        if block["BlockType"]
        in [
            "WORD",
            "LINE",
            "PARAGRAPH",
            "LAYOUT_TITLE",
            "LAYOUT_HEADER",
            "LAYOUT_FOOTER",
            "LAYOUT_SECTION_HEADER",
            "LAYOUT_SECTION",
        ]
    ]


def parse_tables(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    block_map: Dict[str, Dict[str, Any]] = {b["Id"]: b for b in blocks}
    tables = []
    for block in blocks:
        if block["BlockType"] == "TABLE":
            cells = []
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for cell_id in rel["Ids"]:
                        if cell_id in block_map:
                            cell = block_map[cell_id]
                            cells.append(
                                {
                                    "id": cell["Id"],
                                    "text": cell.get("Text", ""),
                                    "row_index": cell.get("RowIndex", 0),
                                    "column_index": cell.get("ColumnIndex", 0),
                                    "row_span": cell.get("RowSpan", 1),
                                    "column_span": cell.get("ColumnSpan", 1),
                                    "confidence": cell.get("Confidence", 0.0),
                                }
                            )
            tables.append(
                {
                    "table_id": block["Id"],
                    "cells": sorted(
                        cells, key=lambda c: (c["row_index"], c["column_index"])
                    ),
                }
            )
    return tables


def parse_key_values(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    block_map: Dict[str, Dict[str, Any]] = {b["Id"]: b for b in blocks}
    kv_pairs = []
    for block in blocks:
        if block["BlockType"] == "KEY_VALUE_SET" and "EntityTypes" in block:
            if block["EntityTypes"][0] == "KEY":
                key_text = block.get("Text", "")
                value_id = None
                for rel in block.get("Relationships", []):
                    if rel["Type"] == "VALUE":
                        value_id = rel["Ids"][0]
                        break
                if value_id and value_id in block_map:
                    value_block = block_map[value_id]
                    value_text = value_block.get("Text", "")
                    kv_pairs.append(
                        {
                            "key": key_text,
                            "value": value_text,
                            "confidence": block.get("Confidence", 0.0),
                        }
                    )
    return kv_pairs
