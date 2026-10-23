from typing import Optional

from google.cloud.pubsub_v1.types import ReceivedMessage

from messaging_client import get_subscriber_client, subscription_path
from messaging_models import ConsumeResult, EventMessage


def consume_event(
    subscription_id: Optional[str] = None,
    max_messages: int = 1,
) -> Optional[ConsumeResult]:
    subscriber = get_subscriber_client()
    sub_path = subscription_path(subscription_id)

    response = subscriber.pull(
        request={
            "subscription": sub_path,
            "max_messages": max_messages,
        },
        timeout=30.0,
    )

    if not response.received_messages:
        return None

    received: ReceivedMessage = response.received_messages[0]
    message = received.message

    event = EventMessage.from_json(message.data.decode("utf-8"))
    event.retry_count = received.delivery_attempt

    result = ConsumeResult(
        message_id=message.message_id,
        event=event,
        ack_id=received.ack_id,
        subscription_path=sub_path,
        delivery_attempt=received.delivery_attempt,
    )

    return result


def consume_and_ack(
    subscription_id: Optional[str] = None,
) -> Optional[ConsumeResult]:
    result = consume_event(subscription_id=subscription_id)
    if result and result.ack_id:
        subscriber = get_subscriber_client()
        sub_path = subscription_path(subscription_id)
        subscriber.acknowledge(
            request={
                "subscription": sub_path,
                "ack_ids": [result.ack_id],
            }
        )
    return result
