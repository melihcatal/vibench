import base64
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def encode_document_bytes(data: bytes) -> Dict[str, Any]:
    return {"Bytes": data}


def normalize_blocks(blocks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for block in blocks:
        normalized.append(
            {
                "id": block.get("Id"),
                "block_type": block.get("BlockType"),
                "text": block.get("Text", ""),
                "confidence": block.get("Confidence"),
                "page": block.get("Page"),
                "relationships": block.get("Relationships", []),
                "row_index": block.get("RowIndex"),
                "column_index": block.get("ColumnIndex"),
                "row_span": block.get("RowSpan"),
                "column_span": block.get("ColumnSpan"),
                "entity_types": block.get("EntityTypes", []),
            }
        )
    return normalized


def blocks_to_text(blocks: Iterable[Dict[str, Any]]) -> str:
    parts = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE" and block.get("Text")]
    return "\n".join(parts)


def collect_key_values(blocks: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    kvs = []
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            kvs.append(
                {
                    "key": block.get("Text", ""),
                    "value": block.get("Value", ""),
                }
            )
    return kvs


def make_data_uri(data: bytes, mime_type: str = "application/octet-stream") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(data).decode('utf-8')}"


@dataclass
class DocumentResponse:
    text: str
    blocks: List[Dict[str, Any]]
    raw: Dict[str, Any]
