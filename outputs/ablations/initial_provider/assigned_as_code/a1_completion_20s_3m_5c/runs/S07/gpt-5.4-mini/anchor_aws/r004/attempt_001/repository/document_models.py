from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_bytes(payload: Dict[str, Any]) -> bytes:
    data = payload.get("document_bytes") or payload.get("bytes") or b""
    if isinstance(data, str):
        return data.encode()
    return data


def normalize_region(config: Optional[Dict[str, Any]]) -> Optional[str]:
    if not config:
        return None
    return config.get("region")


def line_texts_from_blocks(blocks: List[Dict[str, Any]]) -> List[str]:
    return [b.get("Text", "") for b in blocks if b.get("BlockType") == "LINE" and b.get("Text")]


def key_value_pairs_from_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET":
            items.append({"id": block.get("Id"), "entity_types": block.get("EntityTypes", []), "confidence": block.get("Confidence")})
    return items
