import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_identifier(value: Any) -> str:
    if value is None:
        raise ValueError("identifier is required")
    text = str(value).strip()
    if not text:
        raise ValueError("identifier is required")
    return text


def normalize_partition_key(value: Any) -> str:
    if value is None:
        raise ValueError("partition_key is required")
    text = str(value).strip()
    if not text:
        raise ValueError("partition_key is required")
    return text


def ensure_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        loaded = json.loads(value)
        if not isinstance(loaded, dict):
            raise ValueError("document payload must decode to an object")
        return loaded
    raise ValueError("document payload must be a dict or JSON object string")


def normalize_document(
    document: Dict[str, Any],
    document_id: Optional[Any] = None,
    partition_key: Optional[Any] = None,
) -> Dict[str, Any]:
    normalized = dict(document)
    if document_id is not None:
        normalized["id"] = normalize_identifier(document_id)
    elif "id" in normalized:
        normalized["id"] = normalize_identifier(normalized["id"])
    else:
        raise ValueError("document id is required")
    if partition_key is not None:
        normalized["partitionKey"] = normalize_partition_key(partition_key)
    elif "partitionKey" in normalized:
        normalized["partitionKey"] = normalize_partition_key(normalized["partitionKey"])
    else:
        normalized["partitionKey"] = normalized["id"]
    normalized.setdefault("updatedAt", utc_now_iso())
    return normalized


def normalize_text_fields(
    document: Dict[str, Any], field_names: List[str]
) -> Dict[str, str]:
    output: Dict[str, str] = {}
    for name in field_names:
        value = document.get(name)
        if value is None:
            continue
        if isinstance(value, str):
            output[name] = value
        else:
            output[name] = json.dumps(value, ensure_ascii=False)
    return output


@dataclass
class DocumentRequest:
    document_id: str
    partition_key: str

    @classmethod
    def create(
        cls, document_id: Any, partition_key: Optional[Any] = None
    ) -> "DocumentRequest":
        normalized_id = normalize_identifier(document_id)
        normalized_pk = normalize_partition_key(
            partition_key if partition_key is not None else normalized_id
        )
        return cls(document_id=normalized_id, partition_key=normalized_pk)


@dataclass
class UpsertRequest:
    document: Dict[str, Any]

    @classmethod
    def create(
        cls,
        document: Any,
        document_id: Optional[Any] = None,
        partition_key: Optional[Any] = None,
    ) -> "UpsertRequest":
        normalized = normalize_document(
            ensure_dict(document), document_id=document_id, partition_key=partition_key
        )
        return cls(document=normalized)


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    limit: int = 25
    partition_key: Optional[str] = None

    @classmethod
    def create(
        cls,
        field_name: str,
        field_value: Any,
        limit: int = 25,
        partition_key: Optional[Any] = None,
    ) -> "QueryRequest":
        name = str(field_name).strip()
        if not name:
            raise ValueError("field_name is required")
        normalized_pk = (
            None if partition_key is None else normalize_partition_key(partition_key)
        )
        return cls(
            field_name=name,
            field_value=field_value,
            limit=max(1, min(int(limit), 100)),
            partition_key=normalized_pk,
        )


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    partition_key: str
    patch_operations: List[Dict[str, Any]] = field(default_factory=list)
    etag: Optional[str] = None

    @classmethod
    def create(
        cls,
        document_id: Any,
        partition_key: Optional[Any],
        patch_operations: List[Dict[str, Any]],
        etag: Optional[str] = None,
    ) -> "ConditionalUpdateRequest":
        if not isinstance(patch_operations, list) or not patch_operations:
            raise ValueError("patch_operations must be a non-empty list")
        return cls(
            document_id=normalize_identifier(document_id),
            partition_key=normalize_partition_key(
                partition_key if partition_key is not None else document_id
            ),
            patch_operations=patch_operations,
            etag=etag,
        )


@dataclass
class DocumentResult:
    found: bool
    document: Optional[Dict[str, Any]]
    etag: Optional[str] = None
    request_charge: Optional[float] = None


def build_document_result(
    document: Optional[Dict[str, Any]], headers: Optional[Dict[str, Any]] = None
) -> DocumentResult:
    etag = None
    request_charge = None
    if headers:
        etag = headers.get("etag") or headers.get("ETag")
        charge = headers.get("x-ms-request-charge")
        if charge is not None:
            request_charge = float(charge)
    return DocumentResult(
        found=document is not None,
        document=document,
        etag=etag,
        request_charge=request_charge,
    )
