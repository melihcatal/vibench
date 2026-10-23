# consume_event.py
# SAME-SCENARIO: consume a single message from a managed Pub/Sub subscription (Google Cloud Pub/Sub)

import json
from google.cloud import pubsub_v1


def consume_one_message(project_id: str, subscription_id: str) -> dict:
    """Pull one message from a Pub/Sub subscription and return its payload as a Python dict.

    Args:
        project_id: GCP project ID.
        subscription_id: Pub/Sub subscription name.

    Returns:
        The decoded message payload or None if no message is available.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Pull a single message, wait up to 5 seconds
    response = subscriber.pull(request={
        "subscription": subscription_path,
        "max_messages": 1,
        "return_immediately": False,
    })

    if not response.received_messages:
        return None

    # Process the first received message
    received = response.received_messages[0]
    # Decode the data
    message_data = json.loads(received.message.data.decode('utf-8'))
    # Acknowledge the message to remove it from the queue
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})
    return message_data

# Example usage (requires valid credentials and subscription ID)
# payload = consume_one_message("my-gcp-project", "my-subscription")
# if payload:
#     print("Received:", payload)
