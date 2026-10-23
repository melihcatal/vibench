import json
import time
from concurrent.futures import TimeoutError
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import Message, ConsumeResponse


def consume_event(subscription_id: str, timeout: float = 5.0):
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode('utf-8')}")
        print(f"Message ID: {message.message_id}")
        print(f"Attributes: {message.attributes}")
        message.ack()
        print(f"Acknowledged message {message.message_id}")

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    finally:
        subscriber.close()


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # Make sure to create a subscription named 'my-test-subscription' for your topic in your Google Cloud Project
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Replace 'my-test-subscription' with your actual Pub/Sub subscription ID
    consume_event("my-test-subscription", timeout=10.0)
