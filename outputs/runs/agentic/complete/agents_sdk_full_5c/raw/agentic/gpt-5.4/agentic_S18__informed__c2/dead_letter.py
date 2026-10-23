from __future__ import annotations

from typing import Optional

from azure.servicebus import ServiceBusMessage

from messaging_client import create_servicebus_client, get_queue_name
from messaging_models import EventMessage, PublishResult, ensure_dict_payload


DEAD_LETTER_REASON = "ProcessingFailed"
DEAD_LETTER_ERROR = "Forwarded to Azure Service Bus dead-letter queue"


def send_to_dead_letter(payload: dict, *, queue_name: Optional[str] = None, reason: str = DEAD_LETTER_REASON, description: str = DEAD_LETTER_ERROR) -> PublishResult:
    event = EventMessage(payload=ensure_dict_payload(payload), attributes={"dead_letter_reason": reason})
    destination = get_queue_name(queue_name)
    dead_letter_path = f"{destination}/$DeadLetterQueue"
    with create_servicebus_client() as client:
        sender = client.get_queue_sender(queue_name=dead_letter_path)
        with sender:
            message = ServiceBusMessage(
                event.body_bytes(),
                message_id=event.message_id,
                subject="dead-letter",
                application_properties={"dead_letter_reason": reason, "dead_letter_error_description": description},
                content_type="application/json",
            )
            sender.send_messages(message)
    return PublishResult(message_id=event.message_id, destination=dead_letter_path, status="dead-lettered")
