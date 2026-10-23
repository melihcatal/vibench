from __future__ import annotations

from typing import Any

from azure.servicebus import ServiceBusMessage

from messaging_client import get_queue_name, get_servicebus_client
from messaging_models import BatchPublishResult


def publish_batch(messages: list[dict[str, Any]]) -> BatchPublishResult:
    queue_name = get_queue_name()
    outbound: list[ServiceBusMessage] = []
    message_ids: list[str] = []
    for item in messages:
        message_id = str(item["id"])
        payload = item["payload"]
        attributes = {str(k): str(v) for k, v in item.get("attributes", {}).items()}
        outbound.append(
            ServiceBusMessage(
                body=payload
                if isinstance(payload, str)
                else __import__("json").dumps(payload, ensure_ascii=False),
                message_id=message_id,
                application_properties=attributes,
                content_type="application/json",
                subject=attributes.get("type", "batch-event"),
            )
        )
        message_ids.append(message_id)
    with get_servicebus_client() as client:
        with client.get_queue_sender(queue_name=queue_name) as sender:
            sender.send_messages(outbound)
    return BatchPublishResult(
        provider="azure-servicebus",
        destination=queue_name,
        message_ids=message_ids,
        accepted_count=len(message_ids),
    )
