import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


@dataclass
class MessageRequest:
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        return normalize_payload(self.payload).encode("utf-8")


@dataclass
class MessageResponse:
    message_id: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchRequest:
    messages: List[MessageRequest]


@dataclass
class BatchResponse:
    message_ids: List[str]


def message_to_dict(message: Any) -> Dict[str, Any]:
    data = message.data.decode("utf-8") if getattr(message, "data", None) else ""
    return {"data": data, "attributes": dict(getattr(message, "attributes", {}) or {})}
