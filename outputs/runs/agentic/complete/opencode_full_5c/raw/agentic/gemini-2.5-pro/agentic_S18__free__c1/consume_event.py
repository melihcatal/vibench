import os
from messaging_client import get_pubsub_subscriber_client


def consume_event(project_id: str, subscription_id: str, timeout: float = 10.0):
    subscriber = get_pubsub_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id],
        }
    )

    return received_message.message
