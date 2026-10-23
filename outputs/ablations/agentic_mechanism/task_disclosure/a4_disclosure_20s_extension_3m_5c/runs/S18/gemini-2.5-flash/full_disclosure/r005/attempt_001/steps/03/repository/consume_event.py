
from google.cloud import pubsub_v1
import os

def consume_event(project_id: str, subscription_id: str):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode()}")
        message.ack()
        # For this example, we only want to process one message, so we stop the subscriber.
        # In a real application, you might process multiple messages or have different stopping conditions.
        raise Exception("Stop processing after one message")

    streaming_pull_future = subscriber_client.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}")

    try:
        streaming_pull_future.result()
    except Exception as ex:
        # Expected exception to stop the subscriber after one message.
        if "Stop processing after one message" in str(ex):
            print("Stopped subscriber after consuming one message.")
        else:
            print(f"Listening for messages on {subscription_path} threw an exception: {ex}.")
            streaming_pull_future.cancel()  # Cancel the subscription.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    finally:
        subscriber_client.close()

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Subscription ID
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS set up or authenticated
    # via `gcloud auth application-default login`
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    SUBSCRIPTION_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")

    if not PROJECT_ID or not SUBSCRIPTION_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        consume_event(PROJECT_ID, SUBSCRIPTION_ID)
