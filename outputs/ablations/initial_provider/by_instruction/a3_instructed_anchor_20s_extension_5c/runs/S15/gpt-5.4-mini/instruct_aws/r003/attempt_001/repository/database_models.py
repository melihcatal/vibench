import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if document is None:
        return {}
    return {str(key): value for key, value in document.items() if value is not None}


def json_body(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, str):
        return json.loads(payload)
    return payload if payload is not None else {}


def normalize_key(value: Any) -> str:
    return str(value)


@dataclass
class UpsertResponse:
    document: Dict[str, Any]
    created: bool


@dataclass
class FetchResponse:
    document: Optional[Dict[str, Any]]


@dataclass
class QueryResponse:
    items: List[Dict[str, Any]]


@dataclass
class UpdateResponse:
    document: Dict[str, Any]
    version: Optional[int]
