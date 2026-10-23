import base64
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"message": normalize_text(payload)}


def encode_json_bytes(data: Dict[str, Any]) -> bytes:
    import json

    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def decode_json_bytes(raw: bytes) -> Dict[str, Any]:
    import json

    return json.loads(raw.decode("utf-8"))


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


@dataclass
class PublishResponse:
    message_id: str
    provider: str
    details: Dict[str, Any]


@dataclass
class ConsumeResponse:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    provider: str


@dataclass
class DeadLetterRequest:
    destination: str
    payload: Dict[str, Any]
    reason: str
    attributes: Optional[Dict[str, str]] = None


@dataclass
class BatchItem:
    message_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


def build_event_payload(
    event_type: str, data: Dict[str, Any], source: str
) -> Dict[str, Any]:
    return {
        "event_type": event_type,
        "source": source,
        "timestamp": iso_utc_now(),
        "data": data,
    }


def payload_text(payload: Dict[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, sort_keys=True)
