from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text.strip()
    if isinstance(text, list):
        return "\n".join(normalize_text(item) for item in text if normalize_text(item))
    return str(text).strip()


def normalize_blocks(blocks: Any) -> List[Dict[str, Any]]:
    if not blocks:
        return []
    return [block for block in blocks if isinstance(block, dict)]


@dataclass
class DocumentRequest:
    document_bytes: bytes
    region: Optional[str] = None
    language: Optional[str] = None


@dataclass
class DocumentResponse:
    text: str
    blocks: List[Dict[str, Any]]
    metadata: Dict[str, Any]
