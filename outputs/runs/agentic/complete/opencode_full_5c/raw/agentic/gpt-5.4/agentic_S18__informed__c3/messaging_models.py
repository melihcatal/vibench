from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import json


JsonDict = Dict[str, Any]


@dataclass
class MessageEvent:
    event_id: str
    event_type: str
    source: str
    payload: JsonDict
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), ensure_ascii=False)


@dataclass
class PublishResult:
    message_id: str
    destination: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ConsumedMessage:
    message_id: str
    body: JsonDict
    attributes: Dict[str, str]
    receipt_handle: str
    queue_url: str


@dataclass
class BatchPublishItem:
    entry_id: str
    event: MessageEvent


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    details: List[JsonDict] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class SafetyAssessment:
    safe: bool
    blocked: bool
    category_scores: Dict[str, float]
    provider: str

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str]
    target_language: str
    provider: str

    def to_dict(self) -> JsonDict:
        return asdict(self)


def normalize_message_payload(payload: Any) -> JsonDict:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return json.loads(payload)
    raise TypeError("payload must be a dict or JSON string")


def encode_message_body(event: MessageEvent) -> str:
    return event.to_json()


def decode_message_body(body: str) -> JsonDict:
    return normalize_message_payload(body)
