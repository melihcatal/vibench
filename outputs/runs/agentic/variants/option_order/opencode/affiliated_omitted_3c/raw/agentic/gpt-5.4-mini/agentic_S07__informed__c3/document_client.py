import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import boto3

from document_models import DocumentRequest, LayoutBlock, KeyValuePair, Table, TableCell


def build_textract_client(region_name: Optional[str] = None):
    return boto3.client("textract", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def load_bytes(request: DocumentRequest) -> bytes:
    if request.content is not None:
        return request.content
    if request.base64_content is not None:
        return base64.b64decode(request.base64_content)
    if request.source_path is not None:
        return Path(request.source_path).read_bytes()
    raise ValueError("DocumentRequest requires content, base64_content, or source_path")


def _blocks(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(response.get("Blocks", []))


def normalize_ocr_text(response: Dict[str, Any]) -> str:
    lines = [b.get("Text", "") for b in _blocks(response) if b.get("BlockType") == "LINE" and b.get("Text")]
    return "
".join(lines)


def normalize_layout_blocks(response: Dict[str, Any]) -> List[LayoutBlock]:
    blocks = []
    for b in _blocks(response):
        if b.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_HEADER", "LAYOUT_FOOTER", "LAYOUT_SECTION_HEADER", "LAYOUT_LIST", "LAYOUT_TABLE", "LAYOUT_FIGURE"}:
            blocks.append(LayoutBlock(block_type=b.get("BlockType", ""), text=b.get("Text"), confidence=b.get("Confidence"), geometry=b.get("Geometry"), id=b.get("Id")))
    return blocks


def normalize_tables(response: Dict[str, Any]) -> List[Table]:
    blocks = _blocks(response)
    cell_map = {b.get("Id"): b for b in blocks if b.get("BlockType") == "CELL"}
    tables = []
    for table in [b for b in blocks if b.get("BlockType") == "TABLE"]:
        cells = []
        for rel in table.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for cid in rel.get("Ids", []):
                    cell = cell_map.get(cid)
                    if cell:
                        cells.append(TableCell(row_index=cell.get("RowIndex"), column_index=cell.get("ColumnIndex"), text=cell.get("Text"), confidence=cell.get("Confidence"), id=cell.get("Id")))
        tables.append(Table(cells=cells, id=table.get("Id"), confidence=table.get("Confidence")))
    return tables


def normalize_key_values(response: Dict[str, Any]) -> List[KeyValuePair]:
    blocks = _blocks(response)
    by_id = {b.get("Id"): b for b in blocks if b.get("Id")}
    pairs = []
    for key in [b for b in blocks if b.get("BlockType") == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])]:
        key_text = _collect_text(key, by_id)
        value_text = ""
        for rel in key.get("Relationships", []):
            if rel.get("Type") == "VALUE":
                for vid in rel.get("Ids", []):
                    value = by_id.get(vid)
                    if value:
                        value_text = _collect_text(value, by_id)
        pairs.append(KeyValuePair(key=key_text, value=value_text, confidence=key.get("Confidence"), id=key.get("Id")))
    return pairs


def _collect_text(block: Dict[str, Any], by_id: Dict[str, Dict[str, Any]]) -> str:
    texts = [block.get("Text", "")]
    for rel in block.get("Relationships", []):
        if rel.get("Type") == "CHILD":
            for cid in rel.get("Ids", []):
                child = by_id.get(cid)
                if child and child.get("Text"):
                    texts.append(child["Text"])
    return " ".join(t for t in texts if t)
