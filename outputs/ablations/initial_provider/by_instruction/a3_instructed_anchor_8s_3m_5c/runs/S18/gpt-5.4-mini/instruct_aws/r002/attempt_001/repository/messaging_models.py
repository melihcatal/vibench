from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return json.loads(payload)
    return {"value": payload}


def normalize_message_body(payload: Any) -> str:
    normalized = normalize_payload(payload)
    return json.dumps(normalized, separators=(",", ":"), sort_keys=True)


@dataclass
class PublishRequest:
    topic_arn: str
    payload: Dict[str, Any]
    subject: Optional[str] = None
    message_attributes: Optional[Dict[str, Dict[str, str]]] = None


@dataclass
class PublishResponse:
    message_id: str
    sequence_number: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ConsumeResponse:
    messages: List[Dict[str, Any]]


@dataclass
class BatchPublishItem:
    id: str
    payload: Dict[str, Any]
    subject: Optional[str] = None
    message_attributes: Optional[Dict[str, Dict[str, str]]] = None


@dataclass
class BatchPublishResponse:
    successful: List[PublishResponse]
    failed: List[Dict[str, Any]]
