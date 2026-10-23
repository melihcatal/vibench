from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class EventMessage:
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_pubsub_data(self) -> bytes:
        body = {
            "event_id": self.event_id,
            "payload": self.payload,
            "attributes": self.attributes,
            "ordering_key": self.ordering_key,
            "published_at": datetime.now(timezone.utc).isoformat(),
        }
        return json.dumps(body, separators=(",", ":")).encode("utf-8")


@dataclass
class ConsumedMessage:
    ack_id: str
    message_id: str
    publish_time: Optional[str]
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessingResult:
    message_id: str
    status: str
    detail: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def decode_message_data(raw: bytes) -> Dict[str, Any]:
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (attributes or {}).items():
        normalized[str(key)] = str(value)
    return normalized


def summarize_results(results: List[ProcessingResult]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return {
        "total": len(results),
        "counts": counts,
        "message_ids": [result.message_id for result in results],
    }
