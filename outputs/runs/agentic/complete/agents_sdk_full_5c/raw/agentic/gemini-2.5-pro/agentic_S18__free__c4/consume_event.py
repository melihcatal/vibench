import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from typing import Optional

from messaging_client import get_subscriber_client, get_subscription_path

def consume_one_message(subscription_id: str) -> Optional[pubsub_v1.types.ReceivedMessage]:
    """
    Consumes a single message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.

    Returns:
        The received message object or None if no message is received.
    """
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)
    
    # We pull just one message.
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    print(f"Received: {received_message.message.data.decode('utf-8')}")
    
    # Acknowledging the message to prevent it from being redelivered.
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
    )
    print(f"Acknowledged message: {received_message.ack_id}")

    return received_message

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    SUBSCRIPTION_ID = os.getenv("PUB_SUB_SUBSCRIPTION_ID", "default-subscription")
    consume_one_message(SUBSCRIPTION_ID)
