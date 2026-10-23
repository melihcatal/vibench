from google.cloud import pubsub_v1
import os
import json

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID")

# Initialize Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def consume_event() -> dict:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.

    Returns:
        dict: The deserialized message data. Returns None if no message is available.
    """

    def callback(message):
        message.ack()
        return json.loads(message.data.decode("utf-8"))

    # Pull a single message
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        return None

    message = response.received_messages[0]
    data = callback(message)

    # Acknowledge the message
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [message.ack_id]}
    )

    return data
