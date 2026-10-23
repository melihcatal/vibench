from __future__ import annotations

from typing import Any

from messaging_client import publish_to_sns
from messaging_models import MessageEvent


def publish_event(
    event_id: str,
    event_type: str,
    source: str,
    payload: dict[str, Any],
    attributes: dict[str, str] | None = None,
) -> dict[str, str]:
    event = MessageEvent(
        event_id=event_id,
        event_type=event_type,
        source=source,
        payload=payload,
        attributes=attributes or {},
    )
    ack = publish_to_sns(event)
    return {"destination": ack.destination, "message_id": ack.message_id}
