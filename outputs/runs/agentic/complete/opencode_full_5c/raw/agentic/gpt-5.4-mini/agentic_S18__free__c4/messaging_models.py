from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            loaded = json.loads(payload)
            return loaded if isinstance(loaded, dict) else {"value": loaded}
        except json.JSONDecodeError:
            return {"text": payload}
    return {"value": payload}


def to_json_bytes(payload: Any) -> bytes:
    return json.dumps(
        normalize_payload(payload), ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[PublishRequest]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class SummaryResult:
    total: int
    succeeded: int
    failed: int
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AuditRecord:
    message_id: str
    status: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    provider: str
