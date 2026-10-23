from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    source: str
    mime_type: str = "image/png"
    language: Optional[str] = None
    task: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedLine:
    text: str
    bounding_box: Optional[Dict[str, float]] = None


@dataclass
class NormalizedBlock:
    kind: str
    text: str
    lines: List[NormalizedLine]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class DocumentResponse:
    text: str
    blocks: List[NormalizedBlock]
    raw: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(v) for v in value if normalize_text(v))
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
    return str(value).strip()


def flatten_lines(items: Any) -> List[NormalizedLine]:
    lines: List[NormalizedLine] = []
    if not isinstance(items, list):
        return lines
    for item in items:
        if isinstance(item, dict):
            lines.append(NormalizedLine(text=normalize_text(item.get("text") or item.get("content")), bounding_box=item.get("boundingBox") or item.get("bounding_box")))
        else:
            text = normalize_text(item)
            if text:
                lines.append(NormalizedLine(text=text))
    return lines


def normalize_blocks(payload: Dict[str, Any]) -> List[NormalizedBlock]:
    blocks: List[NormalizedBlock] = []
    for block in payload.get("blocks", []) if isinstance(payload, dict) else []:
        if isinstance(block, dict):
            lines = flatten_lines(block.get("lines", []))
            blocks.append(NormalizedBlock(kind=normalize_text(block.get("kind") or block.get("type")) or "block", text=normalize_text(block.get("text") or block.get("content")), lines=lines, metadata=block.get("metadata")))
    return blocks
