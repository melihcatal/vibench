import json
import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

def consume_one_message(project_id: str, subscription_id: str, timeout: int = 5):
    """Receives one message from a Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message ID: {message.message_id}")
        print(f"Data: {message.data.decode("utf-8")}")
        if message.attributes:
            print(f"Attributes: {message.attributes}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        # Blocks the thread until a message is received or timeout is reached
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()  # Raise the exception again to avoid suppressed exception warning
        print("No messages received within the timeout period.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        subscriber.close()

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        consume_one_message(project_id, subscription_id)
