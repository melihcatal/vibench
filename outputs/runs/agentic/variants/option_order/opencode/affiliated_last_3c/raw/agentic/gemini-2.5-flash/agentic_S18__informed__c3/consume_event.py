import os
import json
from concurrent.futures import TimeoutError
from messaging_client import PubSubClient
from messaging_models import EventMessage


def consume_one_message(subscription_id: str, timeout: int = 5):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    client = PubSubClient()
    subscriber = client.get_subscriber_client()
    subscription_path = subscriber.subscription_path(client.project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message ID: {message.message_id}")
        print(f"Data: {message.data.decode('utf-8')}")
        if message.attributes:
            print(f"Attributes: {message.attributes}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        print("No message received within the timeout period.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        raise e


if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Create a subscription first, e.g., 'my-test-subscription' for 'my-test-topic'
    # gcloud pubsub subscriptions create my-test-subscription --topic my-test-topic

    subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID", "my-test-subscription")
    consume_one_message(subscription_id)
