from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if document is None:
        return {}
    if "id" not in document and "document_id" in document:
        document = dict(document)
        document["id"] = document["document_id"]
    return document


@dataclass
class DocumentRequest:
    id: str
    partition_key: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    etag: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
