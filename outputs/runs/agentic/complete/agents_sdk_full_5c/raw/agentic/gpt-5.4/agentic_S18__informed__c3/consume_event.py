from __future__ import annotations

from typing import Any, Dict, Optional
import json

from messaging_client import MessagingConfig, get_servicebus_client
from messaging_models import ConsumedMessage



def consume_one_event(max_wait_time: int = 5) -> Optional[ConsumedMessage]:
    config = MessagingConfig()
    with get_servicebus_client(config) as client:
        receiver = client.get_queue_receiver(queue_name=config.queue_name, max_wait_time=max_wait_time)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=max_wait_time)
            if not messages:
                return None
            message = messages[0]
            raw_body = b"".join(bytes(part) for part in message.body).decode("utf-8")
            decoded = json.loads(raw_body)
            receiver.complete_message(message)
            return ConsumedMessage(
                message_id=str(message.message_id or decoded.get("message_id", "")),
                body=decoded.get("body", decoded),
                attributes=dict(message.application_properties or {}),
                raw_body=raw_body,
            )



def consume_event_dict(max_wait_time: int = 5) -> Optional[Dict[str, Any]]:
    message = consume_one_event(max_wait_time=max_wait_time)
    if message is None:
        return None
    return {
        "provider": "Azure Service Bus",
        "message_id": message.message_id,
        "body": message.body,
        "attributes": message.attributes,
    }
