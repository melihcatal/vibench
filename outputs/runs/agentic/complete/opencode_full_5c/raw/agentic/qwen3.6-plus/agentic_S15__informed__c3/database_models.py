from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class UpsertRequest:
    document_id: str
    data: dict
    extra_fields: dict | None = None


@dataclass
class UpsertResponse:
    document_id: str
    action: str
    matched_count: int
    modified_count: int
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FetchRequest:
    document_id: str


@dataclass
class FetchResponse:
    document_id: str
    data: dict | None
    found: bool
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class QueryRequest:
    field: str
    value: str
    partition_key: str | None = None
    limit: int = 50


@dataclass
class QueryResultItem:
    document_id: str
    data: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class QueryResponse:
    field: str
    value: str
    partition_key: str | None
    items: list[QueryResultItem]
    total_count: int
    error: str | None = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result["items"] = [item.to_dict() for item in self.items]
        return result


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: dict
    expected_version: int | None = None
    condition_field: str | None = None
    condition_value: str | None = None


@dataclass
class ConditionalUpdateResponse:
    document_id: str
    matched: bool
    modified: bool
    reason: str | None = None
    current_version: int | None = None
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_document_data(raw_data: dict) -> dict:
    normalized = {}
    for key, value in raw_data.items():
        if key.startswith("$"):
            continue
        if isinstance(value, str):
            normalized[key] = value.strip()
        elif isinstance(value, (int, float, bool, type(None))):
            normalized[key] = value
        elif isinstance(value, list):
            normalized[key] = [
                item.strip() if isinstance(item, str) else item for item in value
            ]
        elif isinstance(value, dict):
            normalized[key] = normalize_document_data(value)
        else:
            normalized[key] = str(value)
    return normalized


def build_response_payload(
    status: str, data: Any = None, error: str | None = None
) -> dict:
    payload = {"status": status}
    if data is not None:
        payload["data"] = data
    if error:
        payload["error"] = error
    return payload
