import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_project_id


def consume_event(subscription_id: str, timeout: int = 5):
    """Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A dictionary representing the consumed message, or None if no message is received.
    """
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=timeout,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    message = response.received_messages[0].message
    print(f"Received message: {message.data.decode('utf-8')}")
    print(f"Message attributes: {message.attributes}")

    # Acknowledge the message
    ack_ids = [msg.ack_id for msg in response.received_messages]
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )
    print(f"Acknowledged message ID: {message.message_id}")

    return {
        "data": json.loads(message.data.decode("utf-8")),
        "attributes": dict(message.attributes),
        "message_id": message.message_id,
    }
