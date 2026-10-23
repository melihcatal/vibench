from dataclasses import dataclass


def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict):
        return {k: v for k, v in document.items() if v is not None}
    return document


@dataclass
class UpsertRequest:
    document_id: str
    document: dict


@dataclass
class FetchResponse:
    found: bool
    document: dict | None


@dataclass
class QueryRequest:
    field_name: str
    field_value: object


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: dict
    expected_version: int | None = None
