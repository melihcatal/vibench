from google.cloud import pubsub_v1
import os

# Set your Google Cloud Project ID and Subscription ID
# Replace with your actual project ID and subscription ID
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
subscription_id = os.environ.get("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")

if not project_id or not subscription_id:
    print("Please set the GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID environment variables.")
    exit()

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` converts the project ID and subscription ID into a properly formatted string
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def consume_message(timeout=5.0):
    """Consumes one message from a Pub/Sub subscription."""

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        # Blocks the current thread until the timeout is reached or the subscriber is stopped
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        print("No messages received within the timeout period.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"An error occurred: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    finally:
        subscriber.api.transport.close()

if __name__ == "__main__":
    consume_message()
