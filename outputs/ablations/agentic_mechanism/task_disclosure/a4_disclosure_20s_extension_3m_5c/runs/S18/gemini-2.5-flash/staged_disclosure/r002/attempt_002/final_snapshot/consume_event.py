import os
from google.cloud import pubsub_v1
import time

# Replace with your Google Cloud Project ID and Subscription ID
# It's recommended to use environment variables or a configuration management system
# for sensitive information like project and subscription IDs.
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
subscription_id = os.environ.get("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION")

if not project_id or not subscription_id:
    print("Please set the GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION environment variables.")
    exit(1)

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()
    global message_received
    message_received = True

message_received = False

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

# Wrap subscriber.subscribe in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # Blocks the main thread to keep the client alive, but with a timeout for consuming one message
        streaming_pull_future.result(timeout=30)
    except TimeoutError:
        print("No message received within 30 seconds.")
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
    except Exception as e:
        print(f"An error occurred: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

print("Finished consuming message (or timed out).")
