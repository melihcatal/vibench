from __future__ import annotations

from typing import Any, Dict, Iterable, List
import json

from messaging_client import MessagingConfig, build_servicebus_message, get_servicebus_client
from messaging_models import BatchPublishResult, MessageAttributes, PublishEventRequest, normalize_payload



def batch_publish(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    config = MessagingConfig()
    requests: List[PublishEventRequest] = []
    for index, event in enumerate(events, start=1):
        attrs = MessageAttributes(event_type="batch.event", source="pubsub-batch-publisher")
        request = PublishEventRequest(body=normalize_payload(event), attributes=attrs)
        requests.append(request)

    message_ids: List[str] = []
    with get_servicebus_client(config) as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            batch = sender.create_message_batch()
            for request in requests:
                body = request.to_message_body()
                decoded = json.loads(body)
                message_ids.append(decoded["message_id"])
                message = build_servicebus_message(
                    body,
                    message_id=decoded["message_id"],
                    application_properties=request.attributes.to_headers(),
                )
                if not batch.try_add_message(message):
                    sender.send_messages(batch)
                    batch = sender.create_message_batch()
                    if not batch.try_add_message(message):
                        raise ValueError("Message too large for Azure Service Bus batch")
            if len(batch) > 0:
                sender.send_messages(batch)

    result = BatchPublishResult(published_count=len(message_ids), message_ids=message_ids)
    return {
        "provider": "Azure Service Bus",
        "queue": config.queue_name,
        "published_count": result.published_count,
        "message_ids": result.message_ids,
    }
