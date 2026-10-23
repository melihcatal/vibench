from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional


def _to_plain(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    if isinstance(value, tuple):
        return [_to_plain(v) for v in value]
    return value


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    return _to_plain(dict(document))


def normalize_documents(documents: Iterable[Mapping[str, Any]]) -> list[Dict[str, Any]]:
    return [normalize_document(document) for document in documents]


@dataclass(frozen=True)
class DocumentKey:
    identifier: Any
    primary_key: str = "id"

    def as_dict(self) -> Dict[str, Any]:
        return {self.primary_key: self.identifier}


@dataclass(frozen=True)
class UpsertDocumentRequest:
    document: Mapping[str, Any]
    identifier: Optional[Any] = None

    def normalized(self, primary_key: str = "id") -> Dict[str, Any]:
        payload = normalize_document(self.document)
        if self.identifier is not None:
            payload[primary_key] = self.identifier
        return payload


@dataclass(frozen=True)
class ConditionalUpdateRequest:
    key: DocumentKey
    updates: Mapping[str, Any]
    condition: Optional[Mapping[str, Any]] = None
    version_field: str = "version"

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "key": self.key.as_dict(),
            "updates": normalize_document(self.updates),
            "version_field": self.version_field,
        }
        if self.condition is not None:
            payload["condition"] = normalize_document(self.condition)
        return payload


@dataclass(frozen=True)
class FetchDocumentResponse:
    found: bool
    document: Optional[Mapping[str, Any]] = None
    provider: str = "aws-dynamodb"

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"found": self.found, "provider": self.provider}
        if self.document is not None:
            payload["document"] = normalize_document(self.document)
        return payload


@dataclass(frozen=True)
class QueryDocumentsResponse:
    documents: Iterable[Mapping[str, Any]] = field(default_factory=list)
    provider: str = "aws-dynamodb"

    def normalized(self) -> Dict[str, Any]:
        return {"documents": normalize_documents(self.documents), "provider": self.provider}


@dataclass(frozen=True)
class OperationResult:
    ok: bool
    provider: str = "aws-dynamodb"
    status_code: Optional[int] = None
    data: Optional[Mapping[str, Any]] = None

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"ok": self.ok, "provider": self.provider}
        if self.status_code is not None:
            payload["status_code"] = self.status_code
        if self.data is not None:
            payload["data"] = normalize_document(self.data)
        return payload
