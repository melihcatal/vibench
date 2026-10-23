from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    content: str
    mime_type: str = "image/png"
    language_hints: Optional[List[str]] = None


@dataclass
class DocumentResponse:
    text: str
    raw: Dict[str, Any]


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip()


def normalize_pairs(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {str(item.get("key", "")).strip(): item.get("value") for item in items if str(item.get("key", "")).strip()}
