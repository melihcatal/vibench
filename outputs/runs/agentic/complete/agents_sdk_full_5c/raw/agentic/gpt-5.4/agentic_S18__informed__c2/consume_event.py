from __future__ import annotations

from typing import Optional

from messaging_client import create_servicebus_client, get_queue_name, get_subscription_name, get_topic_name
from messaging_models import ConsumedMessage, normalize_json_bytes


def consume_one_message(*, queue_name: Optional[str] = None, topic_name: Optional[str] = None, subscription_name: Optional[str] = None, max_wait_time: int = 5, auto_complete: bool = False) -> Optional[ConsumedMessage]:
    with create_servicebus_client() as client:
        if topic_name:
            receiver = client.get_subscription_receiver(
                topic_name=get_topic_name(topic_name),
                subscription_name=get_subscription_name(subscription_name),
                max_wait_time=max_wait_time,
            )
        else:
            receiver = client.get_queue_receiver(queue_name=get_queue_name(queue_name), max_wait_time=max_wait_time)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=max_wait_time)
            if not messages:
                return None
            message = messages[0]
            body_bytes = b"".join(bytes(part) for part in message.body)
            parsed = normalize_json_bytes(body_bytes)
            result = ConsumedMessage(
                message_id=message.message_id,
                body=parsed,
                delivery_count=getattr(message, "delivery_count", None),
                enqueued_time_utc=str(getattr(message, "enqueued_time_utc", None)) if getattr(message, "enqueued_time_utc", None) else None,
                subject=getattr(message, "subject", None),
                correlation_id=getattr(message, "correlation_id", None),
                raw_text=body_bytes.decode("utf-8"),
            )
            if auto_complete:
                receiver.complete_message(message)
            return result
