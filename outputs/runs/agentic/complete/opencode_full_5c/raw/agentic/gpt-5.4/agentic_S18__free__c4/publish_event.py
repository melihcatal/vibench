from __future__ import annotations

import json
from typing import Any

from azure.servicebus import ServiceBusMessage

from messaging_client import get_queue_name, get_servicebus_client
from messaging_models import EventMessage, PublishResult


def publish_event(
    event_id: str, payload: dict[str, Any], attributes: dict[str, str] | None = None
) -> PublishResult:
    queue_name = get_queue_name()
    event = EventMessage(
        event_id=event_id,
        topic=queue_name,
        payload=payload,
        attributes=attributes or {},
    )
    message = ServiceBusMessage(
        body=event.body_json(),
        message_id=event.event_id,
        application_properties=event.attributes,
        content_type="application/json",
        subject=payload.get("type", "event")
        if isinstance(payload.get("type"), str)
        else "event",
    )
    with get_servicebus_client() as client:
        with client.get_queue_sender(queue_name=queue_name) as sender:
            sender.send_messages(message)
    return PublishResult(
        provider="azure-servicebus",
        destination=queue_name,
        message_id=event.event_id,
        accepted=True,
    )


def publish_event_json(
    event_id: str, payload_json: str, attributes: dict[str, str] | None = None
) -> PublishResult:
    return publish_event(
        event_id=event_id, payload=json.loads(payload_json), attributes=attributes
    )
