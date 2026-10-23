from google.cloud import pubsub_v1
import os

def consume_message(project_id: str, subscription_id: str):
    """Consumes one message from a Pub/Sub subscription."""
    
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.types.PubsubMessage):
        print(f"Received message: {message.data.decode("utf-8")}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely to await messages
            streaming_pull_future.result(timeout=30)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Subscription ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        print("Please set the GOOGLE_CLOUD_PROJECT and PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        consume_message(project_id, subscription_id)
