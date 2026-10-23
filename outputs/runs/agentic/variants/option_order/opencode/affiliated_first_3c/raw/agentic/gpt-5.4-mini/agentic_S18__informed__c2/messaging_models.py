import json
from dataclasses import dataclass
from typing import Any


def normalize_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        return json.loads(payload)
    raise TypeError("Unsupported payload type")


@dataclass(frozen=True)
class PublishRequest:
    body: dict[str, Any]
    content_type: str = "application/json"


@dataclass(frozen=True)
class PublishResponse:
    message_id: str | None


@dataclass(frozen=True)
class ConsumeResponse:
    message_id: str | None
    body: dict[str, Any]
