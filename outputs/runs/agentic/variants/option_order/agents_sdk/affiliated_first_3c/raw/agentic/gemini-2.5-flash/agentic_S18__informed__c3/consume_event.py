from google.cloud import pubsub_v1
import os
import json

def consume_event(project_id: str, subscription_id: str):
    """Receives messages from a Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}. Press Ctrl+C to exit.")

    try:
        streaming_pull_future.result() # Blocks until exception is raised or context manager is exited
    except KeyboardInterrupt:
        streaming_pull_future.cancel() # Triggers the shutdown.
        streaming_pull_future.result() # Blocks until the shutdown is complete.
    finally:
        subscriber.close()

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "my-test-subscription")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        consume_event(PROJECT_ID, SUBSCRIPTION_ID)
