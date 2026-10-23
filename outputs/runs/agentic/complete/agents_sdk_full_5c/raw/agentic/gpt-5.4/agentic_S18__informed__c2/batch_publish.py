from __future__ import annotations

from typing import Any, Iterable, List, Optional

from messaging_client import build_servicebus_message, create_servicebus_client, get_queue_name, get_topic_name
from messaging_models import BatchPublishResult, coerce_messages


def publish_batch(messages: Iterable[Any], *, queue_name: Optional[str] = None, topic_name: Optional[str] = None) -> BatchPublishResult:
    prepared = coerce_messages(messages)
    with create_servicebus_client() as client:
        if topic_name:
            destination = get_topic_name(topic_name)
            sender = client.get_topic_sender(topic_name=destination)
        else:
            destination = get_queue_name(queue_name)
            sender = client.get_queue_sender(queue_name=destination)
        accepted_ids: List[str] = []
        with sender:
            batch = sender.create_message_batch()
            for item in prepared:
                outbound = build_servicebus_message(
                    item.body_bytes(),
                    message_id=item.message_id,
                    subject=item.subject,
                    application_properties=item.attributes,
                    content_type=item.content_type,
                )
                if not batch.try_add_message(outbound):
                    sender.send_messages(batch)
                    batch = sender.create_message_batch()
                    if not batch.try_add_message(outbound):
                        raise ValueError(f"Message {item.message_id} exceeds Azure Service Bus batch size")
                accepted_ids.append(item.message_id)
            if len(batch) > 0:
                sender.send_messages(batch)
    return BatchPublishResult(destination=destination, accepted_message_ids=accepted_ids, status="sent")
