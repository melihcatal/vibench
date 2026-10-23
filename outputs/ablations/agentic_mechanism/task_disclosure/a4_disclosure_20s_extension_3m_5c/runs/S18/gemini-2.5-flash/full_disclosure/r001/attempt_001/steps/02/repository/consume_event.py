
from google.cloud import pubsub_v1
import os

def consume_event(project_id: str, subscription_id: str, timeout: float = 5.0):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode("utf-8")}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        print("No messages received within the timeout period.")
    except Exception as e:
        print(f"Listening for messages on {subscription_path} threw an exception: {e}.")

    subscriber.close()

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Subscription ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.environ.get("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        print("Please set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        consume_event(project_id, subscription_id)
