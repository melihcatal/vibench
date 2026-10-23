from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_document(value: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in value.items():
        if isinstance(v, dict):
            out[k] = normalize_document(v)
        elif isinstance(v, list):
            out[k] = [normalize_document(i) if isinstance(i, dict) else i for i in v]
        else:
            out[k] = v
    return out


def document_from_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_document(item)


@dataclass
class BaseRequest:
    id_field: str = "id"


@dataclass
class UpsertDocumentRequest(BaseRequest):
    document_id: str = ""
    document: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "UpsertDocumentRequest":
        return cls(
            id_field=payload.get("id_field", "id"),
            document_id=str(payload["document_id"]),
            document=dict(payload.get("document", {})),
        )


@dataclass
class FetchDocumentRequest(BaseRequest):
    document_id: str = ""

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "FetchDocumentRequest":
        return cls(id_field=payload.get("id_field", "id"), document_id=str(payload["document_id"]))


@dataclass
class QueryDocumentsRequest:
    partition_key: Optional[str] = None
    partition_value: Optional[Any] = None
    field_name: Optional[str] = None
    field_value: Optional[Any] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "QueryDocumentsRequest":
        return cls(
            partition_key=payload.get("partition_key"),
            partition_value=payload.get("partition_value"),
            field_name=payload.get("field_name"),
            field_value=payload.get("field_value"),
        )


@dataclass
class ConditionalUpdateRequest(BaseRequest):
    document_id: str = ""
    updates: Dict[str, Any] = field(default_factory=dict)
    version_field: Optional[str] = None
    expected_version: Optional[Any] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ConditionalUpdateRequest":
        return cls(
            id_field=payload.get("id_field", "id"),
            document_id=str(payload["document_id"]),
            updates=dict(payload.get("updates", {})),
            version_field=payload.get("version_field"),
            expected_version=payload.get("expected_version"),
        )
