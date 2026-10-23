import os
from datetime import datetime, timezone

from google.cloud import pubsub_v1

from messaging_client import (
    get_project_id,
    get_pubsub_subscriber_client,
    subscription_path,
    load_topic_config,
)
from messaging_models import EventMessage, ConsumeResult


def consume_event(
    subscription_name: str | None = None,
    project_id: str | None = None,
    timeout: float = 10.0,
) -> ConsumeResult | None:
    project_id = project_id or get_project_id()
    config = load_topic_config()
    subscription_name = subscription_name or config["subscription_name"]

    subscriber = get_pubsub_subscriber_client()
    sub_path = subscription_path(project_id, subscription_name)

    response = subscriber.pull(
        request={
            "subscription": sub_path,
            "max_messages": 1,
        },
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    event = EventMessage.from_pubsub_data(received.message.data)

    subscriber.acknowledge(
        request={
            "subscription": sub_path,
            "ack_ids": [received.ack_id],
        },
    )

    delivery_attempt = 1
    if "delivery_attempt" in received.message.attributes:
        delivery_attempt = int(received.message.attributes["delivery_attempt"])

    return ConsumeResult(
        message_id=received.message.message_id,
        event=event,
        ack_id=received.ack_id,
        delivery_attempt=delivery_attempt,
        received_at=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    result = consume_event()
    if result:
        print(result.to_dict())
    else:
        print("No messages available")
