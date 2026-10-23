from __future__ import annotations

from azure.servicebus import ServiceBusMessage

from messaging_client import get_queue_name, get_servicebus_client
from messaging_models import EventMessage, PublishResult


def send_to_dead_letter(
    event_id: str, payload: dict, attributes: dict[str, str] | None = None
) -> PublishResult:
    dead_letter_queue = get_queue_name("AZURE_SERVICEBUS_DEAD_LETTER_QUEUE_NAME")
    event = EventMessage(
        event_id=event_id,
        topic=dead_letter_queue,
        payload=payload,
        attributes=attributes or {},
    )
    message = ServiceBusMessage(
        body=event.body_json(),
        message_id=event.event_id,
        application_properties={
            **event.attributes,
            "dead_letter_reason": "processing_failed",
        },
        content_type="application/json",
        subject="dead-letter",
    )
    with get_servicebus_client() as client:
        with client.get_queue_sender(queue_name=dead_letter_queue) as sender:
            sender.send_messages(message)
    return PublishResult(
        provider="azure-servicebus",
        destination=dead_letter_queue,
        message_id=event.event_id,
        accepted=True,
    )
