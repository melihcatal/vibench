from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


@dataclass
class PublishRequest:
    topic_path: str
    event: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    topic_path: str
    messages: List[Dict[str, Any]]


@dataclass
class ConsumeRequest:
    subscription_path: str
    max_messages: int = 1


@dataclass
class DeadLetterRequest:
    topic_path: str
    failed_message: Dict[str, Any]
    reason: str


@dataclass
class IntegrationResponse:
    provider: str
    resource: str
    message_ids: List[str] = field(default_factory=list)
    message: Dict[str, Any] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)
