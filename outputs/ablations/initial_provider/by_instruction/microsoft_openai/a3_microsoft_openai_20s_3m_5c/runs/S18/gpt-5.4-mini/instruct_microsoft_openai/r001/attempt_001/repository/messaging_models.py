from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class MessageEnvelope:
    message_id: str
    topic: str
    payload: dict[str, Any]
    attributes: dict[str, str]
    created_at: str


@dataclass
class PublishResult:
    message_id: str
    provider: str
    status: str
    metadata: dict[str, Any]


@dataclass
class ConsumptionResult:
    message_id: str | None
    provider: str
    payload: dict[str, Any] | None
    attributes: dict[str, str]
    ack_id: str | None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_attributes(attributes: dict[str, Any] | None) -> dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


def normalize_payload(payload: Any) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def envelope_to_dict(envelope: MessageEnvelope) -> dict[str, Any]:
    return asdict(envelope)
