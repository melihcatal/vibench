from messaging_client import get_subscriber, subscription_path
from messaging_models import ConsumedMessage, normalize_attributes


def consume_event(subscription: str, timeout: float = 10.0) -> ConsumedMessage | None:
    subscriber = get_subscriber()
    response = subscriber.pull(
        request={"subscription": subscription_path(subscription), "max_messages": 1},
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    message = received.message
    subscriber.acknowledge(
        request={
            "subscription": subscription_path(subscription),
            "ack_ids": [received.ack_id],
        }
    )
    return ConsumedMessage(
        message_id=message.message_id,
        payload=message.data.decode("utf-8"),
        attributes=normalize_attributes(message.attributes),
    )
