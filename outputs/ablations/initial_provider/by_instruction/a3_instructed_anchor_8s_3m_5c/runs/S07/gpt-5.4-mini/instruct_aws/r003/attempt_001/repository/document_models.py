from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    bucket: str
    key: str
    version: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextExtractionResult:
    text: str
    lines: List[str]
    pages: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class LayoutExtractionResult:
    blocks: List[Dict[str, Any]]
    lines: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class KeyValueExtractionResult:
    key_values: Dict[str, str]
    raw: Dict[str, Any]


def normalize_textract_blocks(blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    lines = []
    blocks_by_type = {"WORD": [], "LINE": [], "TABLE": [], "CELL": [], "KEY_VALUE_SET": []}
    for block in blocks:
        btype = block.get("BlockType")
        if btype == "LINE":
            lines.append(block.get("Text", ""))
        if btype in blocks_by_type:
            blocks_by_type[btype].append(block)
    return {"lines": lines, "blocks_by_type": blocks_by_type}


def kv_from_textract(blocks: List[Dict[str, Any]]) -> Dict[str, str]:
    index = {b.get("Id"): b for b in blocks if b.get("Id")}
    keys = [b for b in blocks if b.get("BlockType") == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])]
    values = [b for b in blocks if b.get("BlockType") == "KEY_VALUE_SET" and "VALUE" in b.get("EntityTypes", [])]
    value_by_id = {v.get("Id"): v for v in values if v.get("Id")}

    def text_of(block: Dict[str, Any]) -> str:
        words = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for cid in rel.get("Ids", []):
                    child = index.get(cid)
                    if child and child.get("BlockType") == "WORD":
                        words.append(child.get("Text", ""))
        return " ".join(w for w in words if w)

    def value_text(block: Dict[str, Any]) -> str:
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "VALUE":
                for vid in rel.get("Ids", []):
                    value = value_by_id.get(vid)
                    if value:
                        return text_of(value)
        return ""

    return {text_of(k): value_text(k) for k in keys if text_of(k)}
