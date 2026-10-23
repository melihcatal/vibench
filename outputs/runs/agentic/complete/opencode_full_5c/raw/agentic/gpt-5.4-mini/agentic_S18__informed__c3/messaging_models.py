from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"text": str(payload)}


def normalize_topic_name(topic: str) -> str:
    return topic.strip()


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


@dataclass
class PublishResponse:
    message_id: str


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[Dict[str, Any]]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class DeadLetterRequest:
    destination: str
    original_message_id: str
    payload: Dict[str, Any]
    reason: str


@dataclass
class MessageRecord:
    message_id: str
    status: str
    payload: Dict[str, Any]
