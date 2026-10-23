import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_subscription_path


def consume_one_event(subscription_id: str, timeout: float = 5.0):
    """Consumes a single message from a Google Cloud Pub/Sub subscription."""
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)

    message_data = None

    def callback(message):
        nonlocal message_data
        message_data = message.data
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()  # Block until the shutdown is complete

    return message_data


if __name__ == "__main__":
    subscription_id = os.environ.get("GCP_SUBSCRIPTION_ID", "default-subscription")
    print(f"Consuming one message from {subscription_id}...")
    message = consume_one_event(subscription_id)
    if message:
        print(f"Received message: {message.decode('utf-8')}")
    else:
        print("No message received within the timeout period.")
