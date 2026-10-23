from google.cloud import pubsub_v1
import os
import json

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
subscription_id = os.getenv("GOOGLE_CLOUD_SUBSCRIPTION_ID")

# Initialize Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def consume_event() -> dict:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.

    Returns:
        dict: The decoded message data as a dictionary.

    Raises:
        Exception: If no message is received or an error occurs.
    """

    def callback(message):
        message.ack()
        nonlocal received_message
        received_message = json.loads(message.data.decode("utf-8"))

    received_message = None
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        # Wait for a message to be received
        streaming_pull_future.result(timeout=10.0)
    except Exception as e:
        streaming_pull_future.cancel()
        raise Exception(f"Failed to consume message: {e}")
    finally:
        subscriber.close()

    if received_message is None:
        raise Exception("No message received within the timeout period.")

    return received_message
