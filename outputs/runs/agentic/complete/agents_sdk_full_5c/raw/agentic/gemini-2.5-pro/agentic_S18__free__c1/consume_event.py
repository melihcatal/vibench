import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from typing import Optional

from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import ReceivedMessage

def consume_one_message() -> Optional[ReceivedMessage]:
    """
    Consumes a single message from a Google Cloud Pub/Sub subscription.

    Returns:
        A ReceivedMessage object or None if no message is received.
    """
    subscription_id = os.getenv("GCP_PUBSUB_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("GCP_PUBSUB_SUBSCRIPTION_ID environment variable not set.")

    subscriber_client = get_subscriber_client()
    subscription_path = get_subscription_path(subscriber_client, subscription_id)

    print(f"Listening for messages on {subscription_path}...")
    
    response = subscriber_client.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    
    # In a real app, you would process the message here before acknowledging.
    print(f"Received message: {received_message.message.data.decode('utf-8')}")
    
    # Acknowledge the message so it's not delivered again.
    subscriber_client.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
    )
    print(f"Acknowledged message: {received_message.ack_id}")

    return ReceivedMessage(
        ack_id=received_message.ack_id,
        data=received_message.message.data,
        attributes=dict(received_message.message.attributes),
    )

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    # To run, set GCP_PROJECT_ID and GCP_PUBSUB_SUBSCRIPTION_ID environment variables.
    # Example:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_PUBSUB_SUBSCRIPTION_ID="your-subscription-id"
    # python consume_event.py
    try:
        consume_one_message()
    except ValueError as e:
        print(e)
