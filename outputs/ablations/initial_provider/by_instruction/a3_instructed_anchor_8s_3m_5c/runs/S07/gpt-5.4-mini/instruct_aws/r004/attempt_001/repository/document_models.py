from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    document_bytes: bytes


@dataclass
class OCRResponse:
    text: str
    blocks: List[Dict[str, Any]]


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def collect_block_text(blocks: List[Dict[str, Any]], block_type: Optional[str] = None) -> str:
    values = []
    for block in blocks:
        if block_type is None or block.get("BlockType") == block_type:
            text = block.get("Text")
            if text:
                values.append(text)
    return normalize_text("\n".join(values))
