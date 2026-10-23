from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union[JsonScalar, "JsonObject", "JsonArray"]
JsonObject = Dict[str, JsonValue]
JsonArray = List[JsonValue]


def normalize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, tuple):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_value(item) for key, item in value.items()}
    return value


def normalize_document(document: Mapping[str, Any]) -> JsonObject:
    return {key: normalize_value(value) for key, value in document.items()}


@dataclass(frozen=True)
class DocumentRequest:
    table_name: str
    primary_key: str = "id"


@dataclass(frozen=True)
class FetchDocumentRequest(DocumentRequest):
    primary_id: Any = None


@dataclass(frozen=True)
class UpsertDocumentRequest(DocumentRequest):
    document: JsonObject = field(default_factory=dict)
    primary_id: Any = None


@dataclass(frozen=True)
class QueryDocumentsRequest(DocumentRequest):
    field_name: str = ""
    field_value: Any = None
    use_partition_key: bool = False
    limit: Optional[int] = None
    index_name: Optional[str] = None


@dataclass(frozen=True)
class ConditionalUpdateRequest(DocumentRequest):
    key: JsonObject = field(default_factory=dict)
    update_expression: str = ""
    expression_attribute_values: JsonObject = field(default_factory=dict)
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[JsonObject] = None


@dataclass(frozen=True)
class DocumentResponse:
    ok: bool
    table: str
    primary_key: str


@dataclass(frozen=True)
class FetchDocumentResponse(DocumentResponse):
    found: bool = False
    primary_id: Any = None
    document: Optional[JsonObject] = None
    response: Optional[JsonObject] = None


@dataclass(frozen=True)
class UpsertDocumentResponse(DocumentResponse):
    primary_id: Any = None
    response: Optional[JsonObject] = None


@dataclass(frozen=True)
class QueryDocumentsResponse(DocumentResponse):
    field_name: str = ""
    field_value: Any = None
    use_partition_key: bool = False
    count: int = 0
    scanned_count: Optional[int] = None
    documents: List[JsonObject] = field(default_factory=list)
    response: Optional[JsonObject] = None


@dataclass(frozen=True)
class ConditionalUpdateResponse(DocumentResponse):
    attributes: JsonObject = field(default_factory=dict)
    response: Optional[JsonObject] = None
