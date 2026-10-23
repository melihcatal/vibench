import os
from google.cloud.pubsub_v1.subscriber.message import Message

from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    get_project_id,
)


def consume_event(subscription_id: str, timeout: float = 10.0):
    """Consumes a single message from a Google Cloud Pub/Sub subscription."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        subscription=subscription_path, max_messages=1, return_immediately=True
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]

    try:
        print(f"Received message: {received_message.message.data.decode('utf-8')}")
        subscriber.acknowledge(
            subscription=subscription_path, ack_ids=[received_message.ack_id]
        )
        print(f"Acknowledged message: {received_message.ack_id}")
        return received_message.message.data
    except Exception as e:
        print(f"Error processing message: {e}")
        subscriber.nack(
            subscription=subscription_path, ack_ids=[received_message.ack_id]
        )
        return None


if __name__ == "__main__":
    # This is an example, and will not be executed.
    SUBSCRIPTION_ID = os.environ.get("PUB_SUB_SUBSCRIPTION", "my-subscription")
    consume_event(SUBSCRIPTION_ID)
