import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def parse_json_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload:
        return json.loads(payload)
    return {}


@dataclass
class PublishRequest:
    topic_arn: str
    message: Any
    subject: Optional[str] = None
    attributes: Optional[Dict[str, Dict[str, str]]] = None


@dataclass
class PublishResponse:
    message_id: str
    request_id: Optional[str] = None


@dataclass
class ConsumeResponse:
    messages: List[Dict[str, Any]]


@dataclass
class AuditRecord:
    record_id: str
    payload: Dict[str, Any]
