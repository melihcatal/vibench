from dataclasses import dataclass, field
from typing import Any


def normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


@dataclass
class DocumentRequest:
    document_id: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    document_id: str
    data: dict[str, Any]
    found: bool = True
