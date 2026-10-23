from typing import TypedDict, Dict, List, Any
import os


class PlainText(TypedDict):
    text: str


class LayoutBlock(TypedDict):
    block_type: str
    text: str
    confidence: float
    bbox: Dict[str, float]


class Table(TypedDict):
    rows: List[List[str]]


class KeyValue(TypedDict):
    key: str
    value: str
    confidence: float


def _get_block_text(block: Dict[str, Any], blocks: List[Dict[str, Any]]) -> str:
    text = block.get("Text", "")
    if text:
        return text
    text_parts = []
    if "Relationships" in block:
        for rel in block["Relationships"]:
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    child_block = next((b for b in blocks if b["Id"] == child_id), {})
                    text_parts.append(_get_block_text(child_block, blocks))
    return " ".join(text_parts).strip()


def normalize_text(response: Dict[str, Any]) -> PlainText:
    blocks = response["Blocks"]
    lines = [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
    return {"text": "\n".join(lines)}


def normalize_layout(response: Dict[str, Any]) -> List[LayoutBlock]:
    blocks = response["Blocks"]
    layout_blocks = []
    for block in blocks:
        if block["BlockType"] in ["PAGE", "LINE", "WORD"]:
            bbox = block["Geometry"]["BoundingBox"]
            layout_blocks.append(
                {
                    "block_type": block["BlockType"],
                    "text": block.get("Text", ""),
                    "confidence": block["Confidence"],
                    "bbox": {
                        "width": bbox["Width"],
                        "height": bbox["Height"],
                        "left": bbox["Left"],
                        "top": bbox["Top"],
                    },
                }
            )
    return layout_blocks


def normalize_tables(response: Dict[str, Any]) -> List[Table]:
    blocks = response["Blocks"]
    tables = []
    for block in blocks:
        if block["BlockType"] == "TABLE":
            cells = []
            if "Relationships" in block:
                for rel in block["Relationships"]:
                    if rel["Type"] == "CHILD":
                        for child_id in rel["Ids"]:
                            cell_block = next(
                                (b for b in blocks if b["Id"] == child_id), None
                            )
                            if cell_block:
                                cells.append(cell_block)
            cells.sort(key=lambda c: (c.get("RowIndex", 0), c.get("ColumnIndex", 0)))
            rows = []
            current_row = []
            prev_row_idx = -1
            for cell in cells:
                row_idx = cell.get("RowIndex", 0)
                if row_idx != prev_row_idx:
                    if current_row:
                        rows.append(current_row)
                    current_row = []
                    prev_row_idx = row_idx
                cell_text = _get_block_text(cell, blocks)
                current_row.append(cell_text)
            if current_row:
                rows.append(current_row)
            tables.append({"rows": rows})
    return tables


def normalize_key_values(response: Dict[str, Any]) -> List[KeyValue]:
    blocks = response["Blocks"]
    key_map: Dict[str, str] = {}
    value_map: Dict[str, str] = {}
    for block in blocks:
        if block["BlockType"] == "KEY_VALUE_SET":
            entity_types = [et["Type"] for et in block.get("EntityTypes", [])]
            block_text = _get_block_text(block, blocks)
            block_id = block["Id"]
            if "KEY" in entity_types:
                key_map[block_id] = block_text
            if "VALUE" in entity_types:
                value_map[block_id] = block_text
    kvs = []
    for block in blocks:
        if block["BlockType"] == "KEY_VALUE_SET" and block["Id"] in key_map:
            value = None
            block_conf = block.get("Confidence", 0.0)
            for rel in block.get("Relationships", []):
                if rel["Type"] == "VALUE" and value is None:
                    for v_id in rel["Ids"]:
                        if v_id in value_map:
                            value = value_map[v_id]
                            break
            if value is not None:
                kvs.append(
                    {
                        "key": key_map[block["Id"]],
                        "value": value,
                        "confidence": block_conf,
                    }
                )
    return kvs
