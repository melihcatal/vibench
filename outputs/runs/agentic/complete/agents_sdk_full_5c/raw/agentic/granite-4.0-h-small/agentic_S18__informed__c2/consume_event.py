import os
from google.cloud import pubsub_v1

# Helper client utilities imported from local module
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

def consume_event(subscription_name: str, max_messages: int = 1):
    """Consume up to max_messages messages from a Pub/Sub subscription.

    Args:
        subscription_name (str): Fully qualified subscription name.
        max_messages (int, optional): Number of messages to pull at once.
    """
    client = PubSubClient()
    subscriber = pubsub_v1.SubscriberClient()
    # subscriber = subscriber.subscriber_client_with_credentials(...) if custom auth needed
    future = subscriber.subscribe(subscription_name, callback=receive_message)
    # Run the subscriber for up to max_messages processed
    future.result(timeout=None)  # blocks until max_messages are handled
    print(f"Consumed {max_messages} message(s) from {subscription_name}.")

def receive_message(message: pubsub_v1.subscriber.message.Message):
    """Callback executed for each pulled message."""
    # Wrap raw message in our local model for normalization
    wrapped = PubSubMessage(message)
    print(f"Received message id={wrapped.message_id} data={wrapped.data.decode('utf-8')}")
    # Acknowledge after processing (or send to DLQ if failed)
    message.ack()

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    subscription = f"projects/{project_id}/subscriptions/example-subscription"
    consume_event(subscription, max_messages=5)
