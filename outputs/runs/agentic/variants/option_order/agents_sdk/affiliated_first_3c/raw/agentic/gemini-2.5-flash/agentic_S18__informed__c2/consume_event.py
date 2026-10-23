import json
import os
from google.cloud import pubsub_v1

from messaging_client import get_subscriber_client

def consume_one_event(subscription_id: str, project_id: str = None, timeout: float = 5.0):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id or os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.message_id}")
        print(f"Data: {message.data.decode('utf-8')}")
        print(f"Attributes: {message.attributes}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result() # Raises TimeoutError if the timeout exceeded.
    except Exception as e:
        print(f"Listening for messages on {subscription_path} threw an exception: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # Ensure a subscription named 'my-subscription' exists for 'my-topic'.
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python consume_event.py
    consume_one_event("my-subscription", timeout=10)
