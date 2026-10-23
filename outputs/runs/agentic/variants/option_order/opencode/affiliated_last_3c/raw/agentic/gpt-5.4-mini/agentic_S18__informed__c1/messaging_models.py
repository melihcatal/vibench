from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value).strip()


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, (bytes, str)):
        text = (
            payload.decode("utf-8", errors="replace")
            if isinstance(payload, bytes)
            else payload
        )
        return json.loads(text)
    raise TypeError("payload must be dict, str, bytes, or None")


@dataclass
class MessageEnvelope:
    id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishResult:
    provider: str
    topic: str
    message_id: Optional[str] = None
    message_ids: List[str] = field(default_factory=list)
    status: str = "ok"


@dataclass
class ConsumeResult:
    provider: str
    subscription: str
    message: Optional[MessageEnvelope] = None
    status: str = "empty"


@dataclass
class SafetyResult:
    provider: str
    unsafe: bool
    score: float
    labels: Dict[str, float] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    source_text: str
    translated_text: str
    target_language: str
