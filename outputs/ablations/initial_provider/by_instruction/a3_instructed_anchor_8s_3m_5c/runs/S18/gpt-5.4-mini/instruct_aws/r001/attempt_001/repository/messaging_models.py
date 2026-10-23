import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return "{}"
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def parse_json_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if not payload:
        return {}
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


@dataclass
class PublishRequest:
    message: Dict[str, Any]
    topic_arn: Optional[str] = None
    queue_url: Optional[str] = None


@dataclass
class PublishResponse:
    message_id: str
    destination: str


@dataclass
class BatchMessage:
    id: str
    body: Dict[str, Any]
    attributes: Optional[Dict[str, Any]] = None


@dataclass
class BatchPublishRequest:
    messages: List[BatchMessage]
    topic_arn: Optional[str] = None
    queue_url: Optional[str] = None


@dataclass
class BatchPublishResponse:
    successful: List[Dict[str, Any]]
    failed: List[Dict[str, Any]]


def dataclass_to_dict(value):
    return asdict(value)
