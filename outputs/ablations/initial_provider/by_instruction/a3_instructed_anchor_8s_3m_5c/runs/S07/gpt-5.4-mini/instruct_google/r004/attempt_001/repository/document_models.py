from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    image_bytes: bytes
    mime_type: str = "image/png"
    language_hints: Optional[List[str]] = None


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_kv_pairs(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in pairs or []:
        normalized.append({"key": normalize_text(str(item.get("key", ""))), "value": normalize_text(str(item.get("value", "")))})
    return normalized


def normalize_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for block in blocks or []:
        normalized.append({k: block.get(k) for k in block.keys()})
    return normalized
