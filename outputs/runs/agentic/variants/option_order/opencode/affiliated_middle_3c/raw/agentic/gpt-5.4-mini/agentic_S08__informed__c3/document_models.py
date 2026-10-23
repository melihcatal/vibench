from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    content: bytes
    mime_type: str = "application/pdf"
    filename: Optional[str] = None


@dataclass
class DocumentResponse:
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)


def normalize_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def normalize_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_fields(item) for item in items]
