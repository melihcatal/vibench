from google.cloud import pubsub_v1
import os

# Set your Google Cloud Project ID and subscription name
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
subscription_id = "YOUR_SUBSCRIPTION_ID"  # Replace with your subscription ID

if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message: {message.data.decode()}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # Block indefinitely to listen for messages
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
