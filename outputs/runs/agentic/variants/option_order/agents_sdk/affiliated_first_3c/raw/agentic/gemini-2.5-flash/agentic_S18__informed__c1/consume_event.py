import os
import json
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

def consume_one_message(project_id: str, subscription_id: str, timeout: int = 5):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()
        # In a real application, you might process the message here and then ack it.
        # For this example, we'll just acknowledge and return.
        raise StopIteration # Stop the streaming pull after one message

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        # Block until a message is received or timeout occurs
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        print(f"No message received within {timeout} seconds.")
        streaming_pull_future.cancel()
        streaming_pull_future.result() # Wait for the cancellation to complete
    except StopIteration:
        print("Successfully processed one message.")
    except Exception as e:
        print(f"An error occurred: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == "__main__":
    # For demonstration purposes, replace with your actual project and subscription
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    SUBSCRIPTION_ID = "my-sample-subscription" # Ensure this subscription exists and is linked to the topic
    
    if PROJECT_ID:
        consume_one_message(PROJECT_ID, SUBSCRIPTION_ID)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
