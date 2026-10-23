import json
from typing import Optional
from messaging_client import get_subscription_path, get_subscriber_client
from messaging_models import MessageEvent


def consume_event(
    subscription_id: str = None, timeout: float = 10.0
) -> Optional[MessageEvent]:
    subscription_path = get_subscription_path(subscription_id)
    subscriber = get_subscriber_client()
    response = subscriber.pull(
        subscription=subscription_path,
        max_messages=1,
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    msg_info = response.received_messages[0]
    data = json.loads(msg_info.message.data.decode("utf-8"))
    attributes = (
        dict(msg_info.message.attributes) if msg_info.message.attributes else None
    )
    event = MessageEvent(
        message_id=msg_info.message.message_id, payload=data, attributes=attributes
    )
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[msg_info.ack_id])
    return event
